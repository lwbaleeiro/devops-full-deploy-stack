from fastapi import FastAPI, HTTPException, BackgroundTasks, Form, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import uuid
import logging
import json

# SDKs da Microsoft e RabbitMQ
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.storage.blob import BlobServiceClient
import pika

app = FastAPI(title="Event Management API")

# Setup simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Variáveis de Conexão com fallbacks para os emuladores locais ---
# Chave padrão pública do Cosmos Emulator local
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://localhost:8081")
COSMOS_KEY = os.getenv("COSMOS_KEY", "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==")

# Connection String padrão do Azurite / floci-az local
STORAGE_CONNECTION = os.getenv(
    "STORAGE_CONNECTION_STRING", 
    "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:4577/devstoreaccount1;"
)

RABBITMQ_CONNECTION = os.getenv("RABBITMQ_CONNECTION_STRING", "amqp://admin:admin@localhost:5672/")

# Configurações de banco e filas
DATABASE_NAME = "EventsDB"
CONTAINER_NAME = "EventsContainer"
BLOB_CONTAINER_NAME = "events-backup"
RABBITMQ_QUEUE = "events_queue"

# Variáveis globais para os clientes (inicializadas no startup)
cosmos_client = None
cosmos_container = None
blob_service_client = None

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    date: str
    location: str
    image_url: Optional[str] = None

@app.on_event("startup")
def startup_event():
    global cosmos_client, cosmos_container, blob_service_client
    
    # 1. Conectar ao Cosmos DB (desativando SSL para o emulador local)
    logger.info(f"Conectando ao CosmosDB em: {COSMOS_ENDPOINT}")
    cosmos_client = CosmosClient(
        COSMOS_ENDPOINT, 
        credential=COSMOS_KEY, 
        connection_verify=False # Bypassa erro de certificado SSL do emulador local
    )
    
    try:
        database = cosmos_client.create_database_if_not_exists(id=DATABASE_NAME)
        cosmos_container = database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )
        logger.info("Banco de dados Cosmos e container prontos.")
    except Exception as e:
        logger.error(f"Erro ao inicializar CosmosDB: {e}")

    # 2. Conectar ao Blob Storage
    logger.info("Conectando ao Azure Blob Storage...")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION)
        # Criar o container de blobs se não existir
        try:
            blob_service_client.create_container(BLOB_CONTAINER_NAME)
            logger.info("Container de blob criado.")
        except Exception:
            logger.info("Container de blob já existe.")
    except Exception as e:
        logger.error(f"Erro ao conectar no Blob Storage: {e}")

    # 3. Preparar RabbitMQ (apenas loga e tenta conectar para validar se está de pé)
    logger.info("Testando conexão com RabbitMQ...")
    try:
        publish_to_rabbitmq({"status": "api_started"})
    except Exception as e:
        logger.warning(f"RabbitMQ pode não estar disponível ainda: {e}")


def publish_to_rabbitmq(message_dict: dict):
    """Envia uma mensagem para o RabbitMQ"""
    try:
        params = pika.URLParameters(RABBITMQ_CONNECTION)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message_dict),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        connection.close()
        logger.info(f"Mensagem enviada para a fila {RABBITMQ_QUEUE}")
    except Exception as e:
        logger.error(f"Falha ao enviar mensagem para RabbitMQ: {e}")


def backup_to_blob_storage(event: Event):
    """Salva um arquivo JSON de backup do evento no Blob Storage"""
    if not blob_service_client:
        return
    try:
        blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=f"event-{event.id}.json")
        blob_client.upload_blob(event.json(), overwrite=True)
        logger.info(f"Backup do evento {event.id} salvo no Blob Storage.")
    except Exception as e:
        logger.error(f"Falha ao salvar backup no Storage: {e}")


def cleanup_blob_storage(event_id: str):
    """Deleta os arquivos de backup e imagens associadas ao evento no Blob Storage"""
    if not blob_service_client:
        return
    try:
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        
        # Deleta o JSON de backup
        try:
            container_client.delete_blob(f"event-{event_id}.json")
            logger.info(f"Backup do evento {event_id} deletado do Storage.")
        except Exception:
            pass # Ignora se não existir
            
        # Deleta a imagem (listando pelo prefixo)
        try:
            prefix = f"images/{event_id}-"
            blobs = container_client.list_blobs(name_starts_with=prefix)
            for blob in blobs:
                container_client.delete_blob(blob.name)
                logger.info(f"Imagem {blob.name} deletada do Storage.")
        except Exception:
            pass
            
    except Exception as e:
        logger.error(f"Erro ao deletar arquivos do evento no Storage: {e}")


@app.get("/api/events", response_model=List[Event])
def list_events(search: Optional[str] = None):
    if not cosmos_container:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    try:
        if search:
            # Query simples via SQL do CosmosDB
            query = "SELECT * FROM c WHERE CONTAINS(LOWER(c.title), @search) OR CONTAINS(LOWER(c.description), @search)"
            parameters = [{"name": "@search", "value": search.lower()}]
            items = list(cosmos_container.query_items(
                query=query, parameters=parameters, enable_cross_partition_query=True
            ))
        else:
            items = list(cosmos_container.read_all_items())
            
        return [Event(**item) for item in items]
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/events", response_model=Event)
def create_event(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    image: UploadFile = File(None)
):
    if not cosmos_container:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    event_id = str(uuid.uuid4())
    image_url = None
    
    # Se houver upload de imagem, salva direto no Blob Storage
    if image and image.filename:
        if blob_service_client:
            try:
                blob_name = f"images/{event_id}-{image.filename}"
                blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob=blob_name)
                blob_client.upload_blob(image.file, overwrite=True)
                
                # Monta URL pública para o frontend (assumindo emulador local no host porta 4577)
                image_url = f"http://localhost:4577/devstoreaccount1/{BLOB_CONTAINER_NAME}/{blob_name}"
                logger.info(f"Imagem salva no Storage: {image_url}")
            except Exception as e:
                logger.error(f"Erro ao salvar imagem no Storage: {e}")
                
    event = Event(
        id=event_id,
        title=title,
        description=description,
        date=date,
        location=location,
        image_url=image_url
    )
    
    # 1. Salva no Cosmos DB
    try:
        cosmos_container.create_item(body=event.dict())
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # 2. Processamento assíncrono para Storage e Mensageria (não trava o response)
    background_tasks.add_task(backup_to_blob_storage, event)
    background_tasks.add_task(publish_to_rabbitmq, {"action": "created", "event_id": event.id, "title": event.title})
    
    return event


@app.put("/api/events/{event_id}", response_model=Event)
def update_event(event_id: str, event: Event, background_tasks: BackgroundTasks):
    if not cosmos_container:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    event.id = event_id # garante que o ID é o mesmo da URL
    try:
        cosmos_container.replace_item(item=event_id, body=event.dict())
        
        # Notifica a fila
        background_tasks.add_task(publish_to_rabbitmq, {"action": "updated", "event_id": event.id})
        return event
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Event not found")


@app.delete("/api/events/{event_id}")
def delete_event(event_id: str, background_tasks: BackgroundTasks):
    if not cosmos_container:
        raise HTTPException(status_code=500, detail="Database not connected")
        
    try:
        cosmos_container.delete_item(item=event_id, partition_key=event_id)
        
        # Notifica a fila e limpa os arquivos do storage
        background_tasks.add_task(publish_to_rabbitmq, {"action": "deleted", "event_id": event_id})
        background_tasks.add_task(cleanup_blob_storage, event_id)
        return {"message": "Event deleted successfully"}
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Event not found")
