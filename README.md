# Session Minds Backend API Documentation

## Development

### Database

Models

**Profiles**

**Tools**

**Topics**

**Icons**

**Votes**

**Comments**

**Blacklistet Tokens**

### Deployment

#### Heroku Deployment

**Step 0: Create requirements.txt**

- Create the requirements.txt (pip freeze > requirements.txt)
- Make sure it contains all needed modules and libraries.
- Modify settings.py
  - Add Heroku to ALLOWED_HOSTS
  - Add Frontend adress to CORS_ALLOWED_ORIGINS
  - Set DEBUG to "False"
- Create Procfile in root directory with the following content: web: gunicorn sessionminds.wsgi --log-file -
- Use python manage.py collectstatic in the local IDE terminal to collect all static files

**Step 1: Use Account**

- Create a Heroku account
- Log into the Heroku account

**Step 2: Create New App**

- On the dashboard, click "New" in the upper right corner.
- Select "Create new app"
- Select a name for the application - the name should only contain lowercase letters, numbers, and dashes.
- Choose a region. (Europe as we are in Europe)

**Step 3: Define Deployment Method**

- Select GitHub as deployment method
- Connect GitHub account to Heroku
- Select account and search for repository
- Connect to found repository

**Step 4: Settings**

- Switch to the settings page (Menu in the top)
- Click on "Reveal Config Vars"
- The following Key/Value pairs have been added:
  - ALLOWED_HOSTS
  - CORS_ALLOWED_ORIGINS
  - CLOUDINARY_URL (Created in chapter before)
  - DB_ENGINE
  - DB_HOST
  - DB_OPTIONS
  - DB_PASSWORD
  - DB_PORT
  - DB_SSLMODE
  - DB_USER
  - SECRET_KEY
- In the next section, click on "Add buildpack"
- If not already selected, add Python.

**Step 5: Deploy Application**

- Switch to the deploy page (Menu in the top)
- Look under manual deployment
- Select a branch to deploy (Main in my case)
- Click "Deploy Branch"

**Step 6: Use App**

- Heroku will then set up the virtual environment with all packages, modules and libraries needed. (This can take some time)
- When Heroku is done with the deployment, click "View" and start to use the
- Use app
  <br>

[The deployed version can be found here!](https://sessionminds-be-f5283499a47c.herokuapp.com/)
<br>

### Testing

**(BE) 405 Get method now allowed**

When setting up the backend django rest framework and loading the API URLs using a browser, the PUT and POST views were showing the 405 method and stating, that I was doing a GET request<br>
Nevertheless, I was able to create and update new entries.<br>
This issue continues to happen, but I tried if calling the API using the frontend would lead to a flawless behavior.<br>

**(BE) 403 HTTP 403 Forbidden**

Message shown: "CSRF Failed: CSRF token missing"

When using the Django Rest Framework API Frontend, Updating and Deleting of content is not possible. This might be due to the wrong authentication methode used.
When using the API with JWT, everything works just finde.
