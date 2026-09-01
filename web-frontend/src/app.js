const API_URL = '/api/events';

document.addEventListener('DOMContentLoaded', () => {
    const eventForm = document.getElementById('event-form');
    const eventsContainer = document.getElementById('events-container');
    const searchInput = document.getElementById('search');

    // Load initial events
    fetchEvents();

    eventForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('title', document.getElementById('title').value);
        formData.append('date', document.getElementById('date').value);
        formData.append('location', document.getElementById('location').value);
        formData.append('description', document.getElementById('description').value);
        
        const imageFile = document.getElementById('image').files[0];
        if (imageFile) {
            formData.append('image', imageFile);
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                // Nao setar Content-Type para FormData, o browser seta automaticamente com o boundary correto
                body: formData
            });
            if(response.ok) {
                eventForm.reset();
                fetchEvents();
            }
        } catch (error) {
            console.error('Error creating event:', error);
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
        
        let imageHtml = '';
        if (event.image_url) {
            imageHtml = `<img src="${event.image_url}" alt="${event.title}" style="max-width: 100%; border-radius: 8px; margin-bottom: 10px;">`;
        }

        div.innerHTML = `
            ${imageHtml}
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
