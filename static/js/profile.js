// create the popup element
const popup = document.querySelector('.user-popup');

const profileIcon = document.querySelector('.profile-icon');
const userId = profileIcon.dataset.userId;

// show the popup when the user hovers over the profile icon
profileIcon.addEventListener('mouseenter', async function() {
  // get the user profile data from the server
  const response = await fetch(`/user/${userId}/json/`);
  const profileData = await response.json();

  // update the popup content with the user profile data
  document.querySelector('#popup-username').textContent = profileData.username;
  document.querySelector('#popup-email').textContent = profileData.email;
  document.querySelector('#popup-first-name').textContent = profileData.first_name;
  document.querySelector('#popup-last-name').textContent = profileData.last_name;
  document.querySelector('#popup-home-address').textContent = profileData.home_address;
  document.querySelector('#popup-phone-number').textContent = profileData.phone_number;

  // show the popup
  popup.style.display = 'block';
});

// hide the popup when the user moves the mouse away from the profile icon
profileIcon.addEventListener('mouseleave', function() {
  popup.style.display = 'none';
});

// redirect to the user profile page when the user clicks on the profile icon
profileIcon.addEventListener('click', function() {
  window.location.href = `/accounts/profile/${userId}/`;
});

