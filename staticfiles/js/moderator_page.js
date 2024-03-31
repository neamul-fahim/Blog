const userToken = localStorage.getItem("authToken");
// Fetch users data from API
async function fetchUsers() {
  try {
    const response = await fetch("/get_all_users/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${userToken}`, // Add your token here
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch users");
    }

    const data = await response.json();
    return data.users;
  } catch (error) {
    console.error("Error fetching users:", error);
    return [];
  }
}

// Display users with buttons
async function displayUsers() {
  const usersContainer = document.getElementById("users-container");
  const users = await fetchUsers();

  users.forEach((user) => {
    if (!user.is_superuser) {
      const userDiv = document.createElement("div");
      userDiv.classList.add("user");

      const useremailSpan = document.createElement("span");
      useremailSpan.textContent = user.email;
      userDiv.appendChild(useremailSpan);
      const usernameSpan = document.createElement("span");
      usernameSpan.textContent = user.username;
      userDiv.appendChild(usernameSpan);

      const button = document.createElement("button");
      button.textContent = user.is_moderator
        ? "Remove from Moderator"
        : "Make Moderator";
      button.onclick = async () => {
        try {
          const response = await fetch(`/toggle_moderator/${user.id}/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Token ${userToken}`, // Add your token here
            },
          });

          if (!response.ok) {
            throw new Error("Failed to toggle moderator status");
          }

          // Refresh the page after toggling
          window.location.reload();
        } catch (error) {
          console.error("Error toggling moderator status:", error);
        }
      };
      userDiv.appendChild(button);

      usersContainer.appendChild(userDiv);
    }
  });
}

// Call the displayUsers function when the DOM content is loaded
document.addEventListener("DOMContentLoaded", displayUsers);
