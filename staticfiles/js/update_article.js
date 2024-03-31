      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
              cookieValue = decodeURIComponent(
                cookie.substring(name.length + 1)
              );
              break;
            }
          }
        }
        return cookieValue;
      }

      function getArticleIdFromQuery() {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        return urlParams.get("articleID");
      }

      async function fetchArticleById() {
        try {
          const articleID = getArticleIdFromQuery();
          const userToken = localStorage.getItem("authToken");
          console.log("authToken-----", userToken);
          const response = await fetch(
            `/article/get_article/${articleID}/`,
            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${userToken}`,
              },
            }
          );

          if (!response.ok) {
            throw new Error("Failed to fetch article for editing");
          }

          const article = await response.json();
          populateForm(article);
        } catch (error) {
          console.error("Error fetching article for editing:", error);
        }
      }

      function populateForm(article) {
        document.getElementById("article-title").value = article.title;
        document.getElementById("article-content").value = article.content;
      }

      async function updateArticle() {
        try {
          const articleId = getArticleIdFromQuery();
          const userToken = localStorage.getItem("authToken");
          const csrfToken = getCookie("csrftoken");

          const articleData = {
            title: document.getElementById("article-title").value,
            content: document.getElementById("article-content").value,
          };

          const response = await fetch(
            `/article/update_article/${articleId}/`,
            {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                Authorization: `Token ${userToken}`,
              },
              body: JSON.stringify(articleData),
            }
          );

          if (!response.ok) {
            throw new Error("Failed to update article");
          }

          window.location.href =  '/';
        } catch (error) {
          console.error("Error updating article:", error);
          alert(`Error: ${error.message}`);
        }
      }

      
      document.addEventListener("DOMContentLoaded", () => {
        fetchArticleById();
      });
