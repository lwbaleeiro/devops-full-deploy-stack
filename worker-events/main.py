import pika
import os
import json
import logging
import time

# Configura log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('worker')

RABBITMQ_CONNECTION = os.getenv("RABBITMQ_CONNECTION_STRING", "amqp://admin:admin@localhost:5672/")
RABBITMQ_QUEUE = "events_queue"

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        logger.info(f"🐰 [NOVA MENSAGEM RECEBIDA] Fila: {RABBITMQ_QUEUE}")
        logger.info(f"📦 Payload: {json.dumps(message, indent=2)}")
        
        # Simula um processamento (ex: enviar email, gerar relatorio, etc)
        action = message.get("action", "unknown")
        if action == "created":
            logger.info(f"✅ Evento criado com sucesso (ID: {message.get('event_id')}) -> Enviando email de confirmação de mentirinha...")
        elif action == "updated":
            logger.info(f"🔄 Evento atualizado (ID: {message.get('event_id')}) -> Atualizando caches secundários...")
        elif action == "deleted":
            logger.info(f"🗑️ Evento deletado (ID: {message.get('event_id')}) -> Limpando rastros...")
            
        logger.info("-" * 50)
        
        # Confirma que a mensagem foi processada (ack)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        # Rejeita a mensagem (nack) e não recoloca na fila no caso de erro irreversivel
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    # Aguarda o RabbitMQ subir totalmente antes de tentar conectar
    time.sleep(5) 
    
    logger.info(f"Conectando ao RabbitMQ: {RABBITMQ_CONNECTION.split('@')[-1]}")
    params = pika.URLParameters(RABBITMQ_CONNECTION)
    
    while True:
        try:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            
            # Garante que o worker só pegue 1 mensagem por vez
            channel.basic_qos(prefetch_count=1)
            
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
            
            logger.info(f"[*] Worker iniciado. Aguardando mensagens na fila '{RABBITMQ_QUEUE}'...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Conexão perdida, reconectando em 5 segundos... Erro: {e}")
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Worker parado manualmente.")
            break

if __name__ == '__main__':
    main()
