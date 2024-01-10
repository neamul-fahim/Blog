# .then(data => {
#                 console.log('Failed to sign up')
#                 // Assuming the API returns an object with an 'email' property
#                 var userEmail = formData.get('email');
#                 console.log('User Email:', userEmail);

#                 // Redirect to another page with the email information
#                 console.log('Redirecting to OTP_page');
#                 // Redirect to another page with the email information
#                 window.location.href = '{% url 'OTP_page' %}?email=' + userEmail;
#               })
