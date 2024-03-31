function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function createArticle() {
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    const data = {
      title: title,
      content: content,
    };
    const csrfToken = getCookie("csrftoken");
    const userToken = localStorage.getItem("authToken");
    fetch(`/article/post_article_API/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        Authorization: `Token ${userToken}`,
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "/";
        } else if (response.status === 401) {
          alert(`Please log in to Post Article`);
        } else if (response.status === 403) {
          alert(`You are Banned`);
        } else {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
      })

      .catch((error) => {
        console.error("Error:", error);
        alert(`Error: ${error.message}`);
      });
  }