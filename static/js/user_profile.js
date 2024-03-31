
async function get_user(){
   try{
    const userToken = localStorage.getItem('authToken')
 const response = await fetch('/get_user/',
 {
    method:'GET',
    headers:{
        "Content-Type": "application/json",
        Authorization: `Token ${userToken}`,
    }
 });

 if (!response.ok){
    throw new Error(response.statusText);
 }
 const data = await response.json();

  const user = data.user;
  console.log(user)
  const userEmailElement = document.querySelector('.user-email');
  const userNameElement = document.querySelector('.user-username');
  if (user){
    userEmailElement.textContent=user.email;
    userNameElement.textContent=user.username;
  }
}catch(error){
   console.log(error);
}
}

document.addEventListener('DOMContentLoaded',get_user)