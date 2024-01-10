# <!-- create_article.html -->
# {% extends 'user_management/base.html' %} {% block title %}Create Article
# {%endblock %} {% block content %}

# <h2>Create Article</h2>

# <form id="articleForm" onsubmit="return submitForm(event)">
#   {% csrf_token %} {{ form.as_p }}
#   <button type="submit">Submit</button>
# </form>

# <script>
#   async function fetchUserToken() {
#     try {
#       const userToken = localStorage.getItem("authToken");
#       if (!userToken) {
#         throw new Error("Token not found");
#       }
#       return userToken;
#     } catch (error) {
#       console.error("Error fetching user token:", error);
#       return "";
#     }
#   }

#   async function submitForm(event) {
#     event.preventDefault(); // Prevent the default form submission

#     const userToken = await fetchUserToken();
#     if (!userToken) {
#       console.error("User token not available");
#       return false; // Prevent form submission
#     }

#     const form = document.getElementById("articleForm");
#     const formData = new FormData(form);

#     // Set headers
#     const headers = {
#       "Content-Type": "multipart/form-data", // Set Content-Type for form data
#       Authorization: `Bearer ${userToken}`,
#       "X-CSRFToken": getCSRFToken(), // Include CSRF token
#     };

#     try {
#       const response = await fetch(
#         "http://127.0.0.1:8000/article/post_article_API/",
#         {
#           method: "POST",
#           headers: headers,
#           body: formData,
#         }
#       );

#       // Handle the response
#       if (response.status === 201) {
#         // 201 Created - Successful article creation
#         window.location.href = "{% url 'home_page' %}";
#       } else if (response.status === 400) {
#         // 400 Bad Request - Handle validation errors
#         console.error("Error creating article 400:", response.statusText);
#       } else {
#         // Handle other status codes
#         console.error(
#           "Unexpected response:",
#           response.status,
#           response.statusText
#         );
#       }

#       return false; // Prevent form submission
#     } catch (error) {
#       console.error("Error creating article:", error);
#       return false; // Prevent form submission
#     }
#   }

#   function getCSRFToken() {
#     const csrfTokenElement = document.getElementsByName(
#       "csrfmiddlewaretoken"
#     )[0];
#     return csrfTokenElement ? csrfTokenElement.value : "";
#   }
# </script>

# {% endblock %}
