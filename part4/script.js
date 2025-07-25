document.addEventListener('DOMContentLoaded', () => {
    // --- LOGIN ---
    const main = document.querySelector('main[data-place-id]');
    const placeId = main ? main.getAttribute('data-place-id') : null;

    // Falta definir loginForm si lo necesitas aquí
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            // ... tu lógica de login ...
        });
    }

    // Manejo de review
    const reviewForm = document.querySelector('.add-review .form');
    if (reviewForm && placeId) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const review = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            const token = getCookie('token');

            try {
                const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ review, rating })
                });

                if (response.ok) {
                    alert('Review submitted!');
                    location.reload();
                } else {
                    alert('Error submitting review');
                }
            } catch (error) {
                alert('Network error');
            }
        });
    }

    checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', handlePriceFilter);
    }
}); // <-- ESTA ES LA LLAVE QUE FALTABA

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;

    const token = getCookie('token');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            window.allPlaces = data;
            displayPlaces(data);
        } else {
            console.error('Error fetching places:', response.statusText);
        }
    } catch (error) {
        console.error('Fetch error:', error.message);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place';
        placeDiv.dataset.price = place.price;

        placeDiv.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p><strong>Location:</strong> ${place.location}</p>
            <p><strong>Price:</strong> $${place.price}</p>
        `;

        placesList.appendChild(placeDiv);
    });
}

function handlePriceFilter(event) {
    const selectedPrice = event.target.value;
    const places = document.querySelectorAll('.place');

    places.forEach(place => {
        const price = parseFloat(place.dataset.price);
        if (selectedPrice === 'All' || price <= parseFloat(selectedPrice)) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}