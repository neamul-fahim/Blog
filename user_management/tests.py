<!-- myapp/templates/login.html -->

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login</title>
    <style>
      body {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
        background-color: #f0f0f0;
      }

      .login-container {
        text-align: center;
      }

      form {
        display: inline-block;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        text-align: left;
      }

      label {
        display: block;
        margin-bottom: 8px;
        color: #4b0082; /* Purple color */
      }

      input {
        width: 100%;
        padding: 8px;
        margin-bottom: 16px;
        border: 1px solid #4b0082; /* Purple color */
        border-radius: 4px;
        box-sizing: border-box;
      }

      button {
        background-color: #4b0082; /* Purple color */
        color: #ffffff;
        padding: 10px 20px;
        border: 1px solid #4b0082; /* Purple color */
        border-radius: 4px;
        cursor: pointer;
      }

      button:hover {
        background-color: #6a5acd; /* Lighter purple color on hover */
      }

      .signup-link {
        margin-top: 10px;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div class="login-container">
      <h2>Login</h2>
      <form id="login-form" onsubmit="submitForm(event)">
        {% csrf_token %}
        <label for="username">Username:</label>
        <input type="text" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" name="password" required />
        <button type="submit">Login</button>
      </form>
      <div class="signup-link">
        <p>
          Don't have an account? <a href="{% url 'signup_page' %}">Sign Up</a>
        </p>
      </div>
    </div>

    <script>
      const BASE_API_URL = "{{ BASE_API_URL }}";
      function submitForm(event) {
        // Prevent default form submission
        event.preventDefault();

        // Get form data
        const formData = new FormData(document.getElementById("login-form"));

        // Get CSRF token from the page
        const csrfToken = document.querySelector(
          "[name=csrfmiddlewaretoken]"
        ).value;

        // Make API request using Fetch API
        fetch(`${BASE_API_URL}/login_API/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          credentials: "include",
          body: JSON.stringify(Object.fromEntries(formData)),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            // Store the token in localStorage
            localStorage.setItem("authToken", data.token);

            // Set the Authorization header for future API requests
            const userToken = localStorage.getItem("authToken");

            // Navigate to another page with the Authorization header
            window.location.href = `${BASE_API_URL}/home_page`;
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    </script>
  </body>
</html>
