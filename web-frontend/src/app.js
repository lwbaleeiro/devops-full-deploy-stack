const API_URL = '/api/events';

document.addEventListener('DOMContentLoaded', () => {
    const eventForm = document.getElementById('event-form');
    const eventsContainer = document.getElementById('events-container');
    const searchInput = document.getElementById('search');

    // Carregar eventos iniciais
    fetchEvents();

    eventForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const newEvent = {
            title: document.getElementById('title').value,
            date: document.getElementById('date').value,
            location: document.getElementById('location').value,
            description: document.getElementById('description').value
        };

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newEvent)
            });
            if(response.ok) {
                eventForm.reset();
                fetchEvents();
            }
        } catch (error) {
            console.error('Erro ao criar evento:', error);
            // Fallback para desenvolvimento local sem backend
            renderEvent({...newEvent, id: Date.now().toString()});
        }
    });

    searchInput.addEventListener('input', (e) => {
        fetchEvents(e.target.value);
    });

    async function fetchEvents(search = '') {
        try {
            const response = await fetch(`${API_URL}?search=${search}`);
            const events = await response.json();
            eventsContainer.innerHTML = '';
            events.forEach(renderEvent);
        } catch (error) {
            console.error('Erro ao buscar eventos:', error);
        }
    }

    function renderEvent(event) {
        const div = document.createElement('div');
        div.className = 'event-card';
        div.innerHTML = `
            <h3>${event.title}</h3>
            <p class="date">📅 ${new Date(event.date).toLocaleDateString()}</p>
            <p class="location">📍 ${event.location}</p>
            <p class="description">${event.description}</p>
            <button class="delete-btn" onclick="deleteEvent('${event.id}')">Excluir</button>
        `;
        eventsContainer.appendChild(div);
    }
});

async function deleteEvent(id) {
    if(confirm('Deseja realmente excluir este evento?')) {
        try {
            await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            // Recarregar a página ou re-chamar fetchEvents (simplificado aqui)
            document.location.reload();
        } catch (error) {
            console.error('Erro ao excluir:', error);
        }
    }
}
