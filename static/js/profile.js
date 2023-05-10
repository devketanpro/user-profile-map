 // Fetch user profile data and display it in a popup when hovering over the profile icon
 document.querySelector('.profile-icon').addEventListener('mouseover', function(event) {
    event.preventDefault();
    const userProfileUrl = this.href.replace('/accounts/profile/', '/user/') + 'json/';
    fetch(userProfileUrl)
      .then(response => response.json())
      .then(userProfile => {
        const popup = document.createElement('div');
        popup.className = 'user-popup';
        popup.innerHTML = `
          <div class="user-popup-header">
            <h2>${userProfile.username}</h2>
            <a href="#" class="user-popup-close">&times;</a>
          </div>
          <div class="user-popup-body">
            <p><strong>Email:</strong> ${userProfile.email}</p>
            <p><strong>First Name:</strong> ${userProfile.first_name}</p>
            <p><strong>Last Name:</strong> ${userProfile.last_name}</p>
            <p><strong>Home Address:</strong> ${userProfile.home_address}</p>
            <p><strong>Phone Number:</strong> ${userProfile.phone_number}</p>
          </div>
        `;
        document.body.appendChild(popup);
      })
      .catch(error => console.error(error));
  });
  
  // Redirect to user profile page when clicking the profile icon
  document.querySelector('.profile-icon').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = this.href;
  });
  
  // Close user profile popup when close button is clicked
  document.addEventListener('click', function(event) {
    if (event.target.classList.contains('user-popup-close')) {
      document.querySelector('.user-popup').remove();
    }
  });

//   // Close user profile popup when mouse is moved away from icon
//   document.querySelector('.profile-icon').addEventListener('mouseout', () => {
//     document.querySelector('.user-popup').style.display = 'none';
//   });







