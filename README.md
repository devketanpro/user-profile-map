User Profile Map
This is a Django web application that allows users to create and view user profiles on a map.

Installation
Clone the repository to your local machine
Create a virtual environment and activate it
Install the required packages by running pip install -r requirements.txt
Create a new database by running python manage.py migrate
Start the development server by running python manage.py runserver
Usage
Once the server is running, you can access the application by navigating to http://localhost:8000 in your web browser.

Creating a User Profile
To create a user profile, click the "Sign Up" button on the homepage. Fill in the form with your information and click the "Save" button. Your user profile will be displayed on the map.

Viewing User Location
To view all registered user locations, click the "User Map" button on the homepage. The map will display all user locations on the map that have been created.

Editing a User Profile
To edit your user profile, click on user profile icon on the nav bar right side. It will redirected you to user profile page where you see the "Edit Profile" button to edit user profile.

Testing
To run the tests, run python manage.py test.