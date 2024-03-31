 // Fetch non-moderator users and display them
 async function fetchNonModeratorUsers() {
  try {
    const response = await fetch("/blocked_users/");
    if (!response.ok) {
      throw new Error("Failed to fetch non-moderator users");
    }

    const data = await response.json();
    const users = data.users;

    const usersList = document.getElementById("users-list");

    users.forEach((user) => {
      const userDiv = document.createElement("div");
      userDiv.classList.add("user");

      const userEmail = document.createElement("span");
      userEmail.textContent = `Email: ${user.email}`;

      const userName = document.createElement("span");
      userName.textContent = `Name: ${user.username}`;

      const unblockButton = document.createElement("button");
      unblockButton.textContent = "Unban";
      unblockButton.onclick = async () => {
        try {
          const userToken = localStorage.getItem("authToken");
          const unblockResponse = await fetch(
            `/unblock_user/${user.id}/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${userToken}`,
              },
            }
          );
          if (!unblockResponse.ok) {
            throw new Error("Failed to unblock user");
          }
          // Reload the page after unblocking the user
          location.reload();
        } catch (error) {
          console.error("Error unblocking user:", error);
          alert("Failed to unblock user");
        }
      };

      userDiv.appendChild(userEmail);
      userDiv.appendChild(userName);
      userDiv.appendChild(unblockButton);

      usersList.appendChild(userDiv);
    });
  } catch (error) {
    console.error("Error fetching non-moderator users:", error);
    alert("Failed to fetch non-moderator users");
  }
}

// Call the function to fetch and display non-moderator users when the page loads
window.onload = fetchNonModeratorUsers;
