// Utility: Get a cookie by name
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

// Extract the place ID from the URL
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id'); // returns the place ID
}

// Check if the user is authenticated and show/hide login link (for index.html)
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'inline-block';
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

// Check if user is authenticated on place.html and load place details
function checkPlaceAuthentication(placeId) {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
    if (addReviewSection) {
      addReviewSection.style.display = 'none';
    }
  } else {
    if (addReviewSection) {
      addReviewSection.style.display = 'block';
    }
    fetchPlaceDetails(token, placeId); // Load details only if authenticated
  }
}

// Check auth for review form page, redirect to index if unauthenticated
function checkReviewPageAuth() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
  }
  return token;
}

// Fetch all places from the API (used in index.html)
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    alert('Error loading places: ' + error.message);
  }
}

// Display all places as cards and enable filtering
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = ''; // Clear existing cards

  if (places.length === 0) {
    placesList.innerHTML = '<p style="text-align:center;">No places available yet.</p>';
    return;
  }

  places.forEach(place => {
    const card = document.createElement('div');
    card.classList.add('place-card');
    card.setAttribute('data-price', place.price); // For filtering

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(card);
  });

  setupPriceFilter(); // Enable filtering
}

// Handle the price filter dropdown
function setupPriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;

  priceFilter.addEventListener('change', () => {
    const selected = priceFilter.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseFloat(card.getAttribute('data-price'));

      if (selected === 'all' || price <= parseFloat(selected)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

// Fetch details of a specific place
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (error) {
    alert('Error loading place details: ' + error.message);
  }
}

// Display detailed info about a place
function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  container.innerHTML = '';

  const infoDiv = document.createElement('div');
  infoDiv.classList.add('place-info');

  infoDiv.innerHTML = `
    <h2>${place.name}</h2>
    <p><strong>Price per night:</strong> $${place.price}</p>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
  `;

  container.appendChild(infoDiv);

  displayReviews(place.reviews || []);
}

// Display reviews for the place
function displayReviews(reviews) {
  const reviewSection = document.getElementById('reviews');
  reviewSection.innerHTML = '<h3>Reviews</h3>';

  if (reviews.length === 0) {
    reviewSection.innerHTML += '<p>No reviews yet.</p>';
    return;
  }

  reviews.forEach(review => {
    const card = document.createElement('div');
    card.classList.add('review-card');

    card.innerHTML = `
      <p><strong>${review.user_name}:</strong> ${review.comment}</p>
      <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
    `;

    reviewSection.appendChild(card);
  });
}

// Submit a new review via POST request
async function submitReview(token, placeId, comment, rating) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        place_id: placeId,
        comment: comment,
        rating: parseInt(rating)
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to submit review');
    }

    alert('Review submitted successfully!');
    document.getElementById('review-form').reset();
  } catch (error) {
    alert(`Failed to submit review: ${error.message}`);
  }
}

// Main entry point after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const reviewForm = document.getElementById('review-form');

  // Handle login page
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      if (!email || !password) {
        alert('Please fill in all fields.');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Login failed');
        }

        const data = await response.json();

        // Save JWT in cookie
        document.cookie = `token=${data.access_token}; path=/`;

        // Redirect to index
        window.location.href = 'index.html';
      } catch (error) {
        alert(`Login failed: ${error.message}`);
      }
    });

  // Handle add_review.html logic
  } else if (reviewForm) {
    const token = checkReviewPageAuth();
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const comment = document.getElementById('review-text').value.trim();
      const rating = document.getElementById('review-rating').value;

      if (!comment || !rating) {
        alert('Please fill in all fields.');
        return;
      }

      await submitReview(token, placeId, comment, rating);
    });

  // Handle place.html logic
  } else if (window.location.pathname.includes('place.html')) {
    const placeId = getPlaceIdFromURL();
    checkPlaceAuthentication(placeId);

  // Handle index.html logic
  } else {
    checkAuthentication(); // Check for token and fetch places
  }
});
