# Session Minds Backend API Documentation

This documentation covers the backend and API build with Django and Django Rest Framework.<br>

[Documentation for the Frontend can be found here!](https://github.com/DennisSchenkel/sessionminds-frontend)

## Introduction

Code Institute - Portfolio Project 5 - Advanced Frontend with React<br>

[This paragraph can be found in the frontend documentation](https://github.com/DennisSchenkel/sessionminds-frontend?tab=readme-ov-file#introduction)

[The deployed API can be found here!](https://sessionminds-be-f5283499a47c.herokuapp.com/)

<br>

## Table of Contents

- [Introduction](#introduction)

- [Use Case](#use-case)
- [User Experience](#user-experience)
- [Agile Project Management](#agile-project-management)
- [Development](#development)
  - [Technologies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks](#frameworks)
    - [Modules, Libraries & Plugins](#mudules-libraries--plugins)
    - [Programs & Tools](#programs--tools)
  - [Deployment](#deployment)
    - [Version Control](#version-control)
    - [Cloudinary](#cloudinary)
    - [Database Deployment](#database-deployment)
    - [Heroku Deployment](#heroku-deployment)
  - [Database](#database)
  - [Testing](#testing)
    - [Validator Testing](#validator-testing)
    - [Automated Testing](#automated-testing)
    - [Manual Testing](#manual-testing)
    - [Possible Improvements](#possible-improvements)
    - [Issues During Development](#issues-during-development)
    - [Known Unfixed Bugs](#known-unfixed-bugs)
- [Credits](#credits)
  - [Resources](#resources)
  - [Acknowledgements](#acknowledgements)

## Use Case

[This paragraph can be found in the frontend documentation](https://github.com/DennisSchenkel/sessionminds-frontend?tab=readme-ov-file#use-case)

## User Experience

[This paragraph can be found in the frontend documentation](https://github.com/DennisSchenkel/sessionminds-frontend?tab=readme-ov-file#user-experience)

## Agile Project Management

[This paragraph can be found in the frontend documentation](https://github.com/DennisSchenkel/sessionminds-frontend?tab=readme-ov-file#agile-project-management)

## Development

### Technologies Used

During the development of this application, the following programs and tools have been used.<br>
<br>

- [CI Postgres Database](https://dbs.ci-dbs.net/) (Used for database hosting)
- [Cloudinary](https://cloudinary.com/) (As external hosting services for images)
- [dbdiagram.io](https://dbdiagram.io/) (Creating database visualization)
- [DBeaver](https://dbeaver.io/) (For database inspection and manipulation)
- [Git](https://git-scm.com/) (Version control)
- [GitHub](https://github.com/) (Used as cloud repository)
- [Google Chrome Dev Tools](https://developer.chrome.com/) (Working with console and HTML output)
- [Heroku](https://www.heroku.com/home) (Deployment of final application)
- [Postman](https://www.postman.com/) (For API testing)
- [Visual Studio Code](https://code.visualstudio.com/) (IDE - Integrated Development Environment)

#### Languages

The following languages have been used.<br>
<br>

- Python

#### Frameworks

The following frameworks have been used.<br>
<br>

- Django
- Django Rest Framework

#### Modules, Libraries & Plugins

The following modules, libraries and plugins have been used.<br>
<br>

- AllAuth (For user uthentication)
- Black (Code formatter for Python)
- Cloudinary (Cloud storage for images)
- Gunicorn (Python WSGI HTTP server for UNIX)
- OS (For operating system interaction)
- Pep8 (Check Python code for PEP8 conventions)
- Pillow (For image processing)
- Prettier (Code formatter for JavaScript)
- Psycopg 2 (PostgreSQL adapter for the database)
- Python Slugify (For generating url-slugs)
- Summernote (As a WYSIWYG editor)
- Whitenoise (Middleware for serving static files)

#### Programs & Tools

### Deployment

#### Version Control

This application was developed using Visual Studio Code as the IDE and GitHub for hosting the repository.<br>
<br>
Git was used for version control by using the following comments:<br>
<br>

- git add filename - Select the files that should be uploaded and updated to the GitHub repository.
- git commit -m "commit message" - Commenting the commit to better understand the changes in this specific commit.
- git push - Upload the commit to GitHub.

#### Cloudinary

For using Cloudinary as a hosting provider for images, the following steps have to be conducted:<br>
<br>

- Create a Cloudinary account.
- Login and visit the Cloudinary user account.
- On the bottom left side, click on the gear symbol.
- On the top left, click on "API Keys".
- Click "Generate New API Key" on the top right.
- Update the Django settings.py with API key.
- Use the API in the Heroku deployment settings like described in the next step.

#### Database Deployment

The database for this project was deployed with the help of the [Code Institute Database Maker](https://dbs.ci-dbs.net/).

- **Step 1:** As a student of Code Institute, the email address of the associated student account is entered into the form and sent.
- **Step 2:** An email is sent with the link where all relevant information about the database can be found.
- **Step 3:** Entering the database information into the Django settings and Heroku like mentioned below.

<br>

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

[The deployed API can be found here!](https://sessionminds-be-f5283499a47c.herokuapp.com/)
<br>

### Database

Models

**Profiles**

**Tools**

**Topics**

**Icons**

**Votes**

**Comments**

**Blacklistet Tokens**

### Testing

#### Validator Testing

#### Automated Testing

#### Manuel Testing

#### Possible Improvements

#### Issues During Development

The following backend related issues came up during development but where solved.

**405 Get method now allowed**

Issue:<br>
When setting up the backend Django Rest Framework and loading the API URLs using a browser, views that only existed for PUT and POST were showing the 405 "Method not allowed" error and stating, that a GET request was made.<br>
Nevertheless, creating and updating entries was possible.<br>
This issue continued to happen, but trying to call the API using the frontend would lead to a flawless behavior.<br>

Solution:<br>
The issue seams to stem from using the Django Rest Framework and creating views for only PUT and POST without a GET method. When opening the API endpoint in a browser, a GET request is automatically conducted and the mentioned error is thrown.<br>
Since these views are never to be used directly from a browser, this issue is no not of relevance, but that was a lesson to be learned.<br>

**403 HTTP 403 Forbidden**

Issue:<br>
At the beginning of the project the CSRF method for authentication was used and implemented for using the browser view of the Django Rest Framework. Creating, editing and deleting entries was no issue using this approach.
With adding the frontend application, the authentication method was not implemented correctly. The backend was still using CSRF and the frontend was using JWT for authentication.
This leed to the following message showing when trying to update or delete database entries: "CSRF Failed: CSRF token missing"<br>

Solution:<br>
With implementing JWT in the frontend application and making sure the headers are correct, everything worked just finde.

**Athentication token not deleting**
Issue:<br>
When testing the behavior of the access and the refresh token, an error occurred, showing that the refresh token was valid after its lifetime.<br>

Solution:<br>
A function was created that explicitly checks for the lifetime of the refresh token and blacklists it if the lifetime is excited.<br>

**Login with wrong credentials not showing error & not loading next page**

Issue:<br>
During the development, a modal was used to show the login form. When entering wrong credentials and pressing enter, the modal closed, and the home page was loaded.<br>
Although the wrong login credentials were used, no error was retuned by the API and no error was shown in the login form, that itself disappeared with the closing of the modal.<br>

Solution:<br>
In the backend, the login view was updated and an error response for wrong login credentials was added.<br>
In the frontend, the login modal was exchanged with a complete login page that can not close like a modal, when the form is submitted. Due to not closing the modal with the form, the newly created backend response was used for showing the expected error message.<br>

#### Known Unfixed Bugs

## Credits

### Resources

- All content was written and created by Dennis Schenkel.<br>
- In this project, the Django profile app with its structure is greatly inspired and by the Code Institute examples, although customized in many places.<br>
- When trying to understand concepts and build this full-stack-application, an unlimited amount of Google searches were conducted and various sources like Stack Overflow, Reddit and the different documentations for Django, Bootstrap and React were used.<br>

### Acknowledgements

- Thanks to Gareth McGirr for providing great mentorship as part of the Code Academy course.
- Thanks to Kay for they effort as a facilitator of the Code Institute team.
- Great thanks go to [Dajana Isbaner](https://github.com/queenisabaer) for being the best fellow student I could wish for.
