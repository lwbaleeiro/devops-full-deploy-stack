const API_URL = '/api/events';

document.addEventListener('DOMContentLoaded', () => {
    const eventForm = document.getElementById('event-form');
    const eventsContainer = document.getElementById('events-container');
    const searchInput = document.getElementById('search');

    // Load initial events
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
            console.error('Error creating event:', error);
            // Fallback for local development without backend
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
            console.error('Error fetching events:', error);
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
            <button class="delete-btn" onclick="deleteEvent('${event.id}')">Delete</button>
        `;
        eventsContainer.appendChild(div);
    }
});

async function deleteEvent(id) {
    if(confirm('Are you sure you want to delete this event?')) {
        try {
            await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            // Reload the page or re-call fetchEvents (simplified here)
            document.location.reload();
        } catch (error) {
            console.error('Error deleting:', error);
        }
    }
}
