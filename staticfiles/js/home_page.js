async function fetchArticles(){
    try{
        const response= await fetch("/article/all_articles/");
        if (!response.ok){
            throw new Error("Failed to fetch articles");
        }

        const articles= await response.json();
        return articles;
    }catch(error){
        console.error("Error fetching articles",error);
        return null;
    }

}

async function getUser(){
  try{
    const userToken = localStorage.getItem("authToken");
    const response= await fetch('/get_user/',
    {
      method:'GET',
      headers:{
        "Content-Type": "application/json",
        Authorization: `Token ${userToken}`,
      }
    }
    );
    console.log(response)
    
    const userData= await response.json();

    return userData.user;
  }catch(error){
    console.error("Error fetching articles",error);
        return null;
  }
}

async function displayArticles(){
    const articleContainer= document.getElementById("article-container");
    const loginContainer = document.getElementById("login-username");
    const navbar=document.querySelector(".navbar-menu")

    const articles = await fetchArticles();
    const user = await getUser();
    
    if(articles && articles.length > 0){
        articles.forEach((article)=>{
            const articleCard=document.createElement("div");
            articleCard.setAttribute('class','article-card');
            const formattedDate = new Date(article.created_at)
          .toISOString()
          .split("T")[0];
            articleCard.innerHTML=`
              <div class="article-header">
               <h1>${article.author.username}</h1>
               <div class="author-date">
               <p class="article-title">${article.title}</p>
               <p class="article-date"> ${formattedDate} </p>
               </div>
               </div>
               <div class="article-content">${article.content}</div>
               <div class='article-buttons'>
                 <button class='edit-button' onclick='editArticle(${article.id})'>Edit Article</button>
                 <button class='ban-button' onclick='banAuthor(${article.author.id})'> Ban Author</button>
                 <button class='delete-button' onclick='deleteArticle(${article.id})'> Delete</button>
               </div>
            `;
            articleContainer.appendChild(articleCard);
        })
    }


if (user && (user.is_moderator || user.is_superuser)) {
    // Create a new list item for the "Blocked Users" link
    const blocked_li = document.createElement("li");

    // Create a new anchor element for the link
    const blocked_a = document.createElement("a");
    blocked_a.textContent = "Banned Users"; // Set the text content of the link
    blocked_a.href = '/blocked_users_page/'; // Set the href attribute for the link

    // Append the anchor element to the list item
    blocked_li.appendChild(blocked_a);

    // Append the list item to the navbar
    navbar.appendChild(blocked_li);
}

if (user && user.is_superuser) {
  // Create a new list item for the "Blocked Users" link
  const moderator_li = document.createElement("li");

  // Create a new anchor element for the link
  const moderator_a = document.createElement("a");
  moderator_a.textContent = "Moderator"; // Set the text content of the link
  moderator_a.href = '/moderator_users_page/'; // Set the href attribute for the link

  // Append the anchor element to the list item
  moderator_li.appendChild(moderator_a);

  // Append the list item to the navbar
  navbar.appendChild(moderator_li);
}



    loginContainer.innerHTML = "";

    if (user && user.username) {
      // If user is authenticated, show user's name and logout button
      const usernameContainer = document.createElement("div");
      usernameContainer.classList.add("username-container");
  
      const usernameLink = document.createElement("a");
      usernameLink.textContent = user.username;
      usernameLink.classList.add("username");
      usernameLink.href = "/user_profile_page/"; // Link to user profile page
  
      const logoutButton = document.createElement("button");
      logoutButton.textContent = "Logout";
      logoutButton.classList.add("logout-btn");
      logoutButton.onclick = function() {
          localStorage.removeItem('authToken');
          location.reload(); // Refresh the page after logout
      };
  
      usernameContainer.appendChild(usernameLink);
      usernameContainer.appendChild(logoutButton);
  
      loginContainer.appendChild(usernameContainer);
  }
  
   else {
      console.log('login button')
        // If user is not authenticated, show login button
        const loginBtn = document.createElement("button");
        loginBtn.textContent = "Login";
        loginBtn.classList.add("login-btn"); // Add appropriate class for styling if needed
        loginBtn.onclick = function() {
          window.location.href='/login_page/'
        };
        loginContainer.appendChild(loginBtn);
    }
}

// document.addEventListener('DOMContentLoaded', () => {
//   const dropdownToggle = document.querySelector('.dropdown-toggle');
//   const dropdownMenu = document.querySelector('.dropdown-menu');
 
//   dropdownToggle.addEventListener("click", function() {
//       dropdownMenu.classList.toggle("show");
//   });
//  });
 

async function editArticle(articleID){
  try {
    const authToken = localStorage.getItem("authToken");
    const response = await fetch(`/article/check_permission/${articleID}/`, {
        headers: {
            'Authorization': `Token ${authToken}`
        }
    });
    // Check if the response indicates success
    if (response.ok) {
        // Navigate to the new page
        window.location.href = `/article/update_article_page?articleID=${articleID}`;
    } else {
        // Handle error response
        console.error('Failed to fetch page:', response.statusText);

        throw new Error(`${response.statusText}`);

      }
} catch (error) {
    console.error("Error fetching page:", error);
    alert(`Error: ${error.message}`);

}

}

async function deleteArticle(articleId) {
  console.log('authToken--------========---')

  try {
    const userToken = localStorage.getItem("authToken");
    const response = await fetch(
      `/article/delete_article/${articleId}/`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${userToken}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`${response.statusText}`);
    }

    location.reload();
  } catch (error) {
    console.error("Error deleting article:", error);
    alert(`Error: ${error.message}`);
  }
}

async function banAuthor(authorId) {
  try {
    const userToken = localStorage.getItem("authToken");
    const response = await fetch(
      `/article/ban_author_API/${authorId}/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${userToken}`,
        },
      }
    );


      if (!response.ok) {
        throw new Error(` ${response.statusText}`);
      }
      location.reload();

    // Handle the response as needed
    // After successful response, you may show a confirmation message or take additional actions
  } catch (error) {
    console.error("Error banning author:", error);
    alert(`Error: ${error.message}`);

  }
}

document.addEventListener('DOMContentLoaded',displayArticles);

// home_page.js

// document.addEventListener("DOMContentLoaded", function() {
//   const postArticleLink = document.querySelector("#post-article-link");

//   postArticleLink.addEventListener("click", function(event) {
//     event.preventDefault();
//     const authToken = localStorage.getItem("authToken")
//     // Perform AJAX request to check permission
//     fetch("/get_user/", {
//       method: "GET",
//       headers: {
//         "Content-Type": "application/json",
//         'Authorization': `Token ${authToken}`
//       },
//       credentials: "same-origin" // Include credentials for same-origin requests
//     })
//     .then(response => {
//       if (response.ok) {
//         // Permission granted, redirect to post article page
//         window.location.href = "/article/post_article_page/";
//       } else {
//         // Permission denied, handle error
//         console.error("Permission denied");
//       }
//     })
//     .catch(error => {
//       console.error("Error:", error);
//     });
//   });
// });


