document.addEventListener('DOMContentLoaded', () => {
    // --- LOGIN ---
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:3000/api/v1/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    errorMessage.textContent = error.message || 'Login failed. Please try again.';
                }
            } catch (error) {
                errorMessage.textContent = 'Could not connect to the server.';
                console.error('Login error:', error);
            }
        });
    }

    checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', handlePriceFilter);
    }
});


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
