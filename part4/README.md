# Part 4 - Simple Web Client

This phase focuses on building the front-end of your application using **HTML5**, **CSS3**, and **JavaScript ES6**. The goal is to create an interactive user interface that communicates with your back-end services.

## Objectives

- Develop a user-friendly interface following provided design specifications.
- Implement client-side functionality to interact with the back-end API.
- Ensure secure and efficient data handling using JavaScript.
- Apply modern web development practices for a dynamic web application.

## Learning Goals

- Apply HTML5, CSS3, and JavaScript ES6 in a real-world project.
- Interact with back-end services using AJAX/Fetch API.
- Implement authentication and manage user sessions.
- Enhance user experience with client-side scripting (no page reloads).

## Tasks Breakdown

### 1. Design

- Complete provided HTML and CSS files to match design specs.
- Create pages for:
    - **Login**
    - **List of Places**
    - **Place Details**
    - **Add Review**

### 2. Login

- Implement login using the back-end API.
- Store JWT token in a cookie for session management.

### 3. List of Places

- Display a list of all places.
- Fetch places data from the API.
- Implement client-side filtering by country.
- Redirect to login if user is not authenticated.

### 4. Place Details

- Show detailed view of a place.
- Fetch details from API using place ID.
- Provide access to add review form for authenticated users.

### 5. Add Review

- Implement form to add a review for a place.
- Restrict form access to authenticated users (redirect others to index).

## Note on CORS

When testing your client against your API, you may encounter **CORS errors**. Update your API to allow cross-origin requests.  
See: [Understanding CORS and Flask Configuration](https://flask-cors.readthedocs.io/en/latest/)

## Resources

- [HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript ES6 Features](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Responsive Web Design Basics](https://web.dev/responsive-web-design-basics/)
- [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [Client-Side Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)
