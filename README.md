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
    - [Manual API Testing](#manual-api-testing)
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
- [DBeaver](https://dbeaver.io/) (For database inspection, manipulation and ERD)
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

This section provides a detailed explanation of the custom models in the application, covering the fields in the database tables, how the serializers work, and the functionality of the views.

<details>
<summary>User</summary>
<br>
The default user model from Django is used for user authentication and the profiles associated with each user.<br>
The login method was changed from using the username to using the user's email address as the username.<br>
<br>
</details>

<details>
<summary>Profiles</summary>
<br>

The Profile model stores a user's profile info, with some optional fields for personal and social details. Here's a short overview of the main fields:

**First Name** (optional): Needed for commenting.<br>
**Last Name** (optional): Needed for commenting.<br>
**Profile Description** (optional): A short bio (up to 500 characters).<br>
**Job Title** (optional): User’s job or position.<br>
**Image** (optional, default provided): Profile picture, checked for size, dimensions, and format (JPEG/PNG).<br>
**LinkedIn/Facebook/Instagram/Twitter URLs** (optional): Social media links.<br>
**User** (set automatically): Connects the profile to the user account.<br>
**Tool Count** (auto-set): Counts how many tools the user created.<br>
**Total Votes** (auto-set): Counts how many votes the user's tools have received.<br>
**Slug** (auto-set): A unique, URL-friendly identifier.<br>
**Created/Updated** (auto-set): Timestamps for when the profile was created and last updated.<br>

**Serializer Overview**<br>
**ProfileSerializer**: Handles serializing and validating profile data, with custom methods for checking ownership and validating image uploads.<br>
**UserSerializer**: Handles user data, including email, username, and password updates.<br>
**RegistrationSerializer**: Handles new user registration, ensuring unique emails and matching passwords.<br>
**LoginSerializer**: Manages user login, checking email and password for authentication.<br>

**Profile Views**<br>
**ProfileList**: Retrieves a list of profiles, ordered by tool count or total votes.<br>
**ProfileDetail**: Retrieves, updates, or deletes a profile by profile ID.<br>
**UserProfileView**: Retrieves or updates a profile by user ID.<br>
**UserProfileViewSlug**: Retrieves a profile by its slug.<br>
**UsersListView**: Retrieves a list of all users.<br>
**UserDetailView**: Retrieves a specific user by user ID.<br>
**UserUpdateView**: Updates a user account by user ID.<br>
**UserDeleteView**: Deletes a user account by user ID.<br>

These views help manage user profiles, including updating, retrieving, and deleting profile and user data, while keeping permissions and ownership in place.
<br>

</details>

<details>
<summary>Tools</summary>
<br>

The Tool model represents a resource created by users, and here are the main fields:

**Title** (required): A unique name for the tool (up to 100 characters).<br>
**Short Description** (required): A brief summary of the tool (up to 50 characters).<br>
**Full Description** (required): A detailed description (up to 500 characters).<br>
**Topic** (optional): Links the tool to a topic (default if not set).<br>
**Instructions** (required): How to use the tool (up to 5000 characters).<br>
**Icon** (required): The tool's icon code (default "26aa").<br>
**Slug** (auto-set): A unique, URL-friendly identifier for the tool.<br>
**User** (set automatically): The creator of the tool.<br>
**Created/Updated** (auto-set): Timestamps for when the tool was created and last updated.<br>

**Serializer Overview**<br>
**ToolSerializer**: Handles serializing and validating tools, including fields like is_owner, user, profile, comments, and vote_count. It manages topic_id for setting the tool's topic and includes read-only topic details.<br>

**Tool Views**<br>
**ToolList**: Retrieves all tools, with options to search and order by votes or date, and allows new tools to be created.<br>
**ToolListByUser**: Retrieves all tools made by a certain user.<br>
**ToolDetailById/Slug**: Retrieves, updates, or deletes a tool by its ID or slug.<br>

These views help with tool management, checking ownership, permissions, and supporting pagination.
<br>

</details>

<details>
<summary>Topics & Icons</summary>
<br>

The Topic and Icon models are for categorizing tools and giving these categories(topics) visual icons. Here’s an overview:
<br>

**Topic Model**

The Topic model categorizes tools. It includes the following fields:

**Title** (required): A unique title for the topic (up to 100 characters).<br>
**Description** (optional): A short description (up to 50 characters).<br>
**Icon** (optional): A foreign key to an icon for the topic.<br>
**Slug** (auto-set): A unique, URL-friendly identifier created from the title.<br>
**Created** (auto-set): Timestamp for when the topic was created.<br>
**Updated** (auto-set): Timestamp for when the topic was updated.<br>
<br>

**Icon Model**

The Icon model represents icons that can be assigned to topics. Key fields include:

**Title** (required): A unique name for the icon (up to 100 characters).<br>
**Icon Code** (required): A unique code for the icon (up to 10 characters).<br>

**Serializer Overview**<br>
**TopicSerializer**: Serializes and deserializes topic data, including the icon and a tool_count field that shows how many tools are in the topic.<br>
**IconSerializer**: Serializes icon info, including title and icon_code.<br>

**Topic & Icon Views**<br>
**TopicsList**: Retrieves a list of topics, ordered by tool count or alphabetically, with pagination.<br>
**TopicDetailsBySlug**: Retrieves a specific topic by its slug.<br>
**TopicDetailsById**: Retrieves a topic by its ID, including the tool count.<br>
**ToolsOfTopicBySlug**: Retrieves all tools in a topic, ordered by votes or creation date, with pagination.<br>

These views help manage topics and tools, and the icons visually identify topics.
<br>

</details>

<details>
<summary>Votes</summary>
<br>

The Vote model tracks user votes on tools, ensuring that each user can only vote once for a tool. Key fields include:

**User** (required): A foreign key linking the vote to the user who voted.<br>
**Tool** (required): A foreign key linking the vote to the tool being voted on.<br>
**Created** (auto-set): Timestamp when the vote was made.<br>

**Meta Options**<br>
**unique_together**: Ensures a user can vote only once per tool.<br>
**ordering**: Orders votes by creation date, newest first.<br>

**Serializer Overview**<br>
**VoteSerializer**: Serializes vote data and ensures users can't vote more than once on the same tool. It includes:<br>

- user: A read-only field showing the username of the vote's owner.
- is_owner: A field that checks if the current user owns the vote.

If a user tries to vote more than once on the same tool, an error is raised.

**Vote Views**<br>
**VoteList**: Retrieves all votes and supports creating new votes, with the current user set as the vote owner.<br>
**VoteDetails**: Retrieves or deletes a vote by ID. Only the vote owner can delete it.<br>
**VotesByTool**: Checks if the current user has voted for a tool, and returns the vote's ID if they have.<br>

These views manage tool voting, ensuring users can't vote more than once while allowing them to check their vote status.
<br>

</details>

<details>
<summary>Comments</summary>
<br>

The Comment model tracks comments made by users on tools. Each comment links to a tool and a user. The main fields are:

**Text** (required): The comment's content.<br>
**Tool** (required): A foreign key linking the comment to a tool. Deleting the tool also deletes its comments.<br>
**User** (required): A foreign key linking the comment to the user who made it.<br>
**Created** (auto-set): Timestamp for when the comment was created.<br>
**Updated** (auto-set): Timestamp for the last time the comment was updated.<br>

**Serializer Overview**<br>
**CommentSerializer**: Serializes comment data, including a profile field that provides detailed profile info about the comment's author.<br>

**Comment Views**<br>
**ToolComments**: Retrieves all comments for a tool or lets authenticated users create new comments.<br>

- **GET**: Returns comments for a tool, ordered by creation date.<br>
- **POST**: Lets authenticated users post comments, but they need both a first and last name in their profile.<br>

**CommentDetails**: Retrieves, updates, or deletes a comment by ID. Only the comment's owner can update or delete it.<br>

- **GET**: Returns the details of a specific comment.
- **DELETE**: Deletes the comment if the user owns it.

These views manage comments on tools, allowing users to comment, retrieve, or delete their comments while ensuring permissions are enforced.
<br>

</details>
<br>

The following database diagram was created using DBeaver.

![Sessionminds ER Diagram](/documentation/images/sessionminds-ERD.png)

### Testing

#### Validator Testing

During the development, Flake8 as a plugin for VScode was used to ensure code quality and formatting conventions.
Nevertheless, the code for each python file was tested manually with the CI Python Linter.

<details>
<summary>Sessionminds</summary>
<br>

No errors were found using the CI Python Linter for the project.

![CI Python Linter Results - Sessionminds](/documentation/images/sessionminds-linter.png)

<details>

<details>
<summary>Profiles</summary>
<br>

No errors were found using the CI Python Linter for this app.

![CI Python Linter Results - Profile](/documentation/images/profiles-linter.png)

<details>

<details>
<summary>Tools</summary>
<br>

No errors were found using the CI Python Linter for this app.

![CI Python Linter Results - Tools](/documentation/images/tools-linter.png)

<details>

<details>
<summary>Topics</summary>
<br>

No errors were found using the CI Python Linter for this app.

![CI Python Linter Results - Topics](/documentation/images/topics-linter.png)

<details>

<details>
<summary>Votes</summary>
<br>

No errors were found using the CI Python Linter for this app.

![CI Python Linter Results - Votes](/documentation/images/votes-linter.png)

<details>

<details>
<summary>Comments</summary>
<br>

No errors were found using the CI Python Linter for this app.

![CI Python Linter Results - Comments](/documentation/images/comments-linter.png)

<details>

#### Automated Testing

For this backend/API project were 33 written and passed successfully.

- Authentication(Profile)

- Tools

- Topics

- Votes

- Comments

![Django Automated Testing](/documentation/images/django-automated-testing.png)

**Learning from automated testing**
The automated test for this project were mostly written towards the end of the project. When writing the tests, some minor issues came up, like an authentication issue for deleting comments.<br>
In future projects, the test will be written directly with the application itself like thought in the CI material, to prevent bigger issues from the ground up.

#### Manuel API Testing

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

- Thanks to Gareth McGirr for providing great mentorship and awesome support as part of the Code Academy course.
- Thanks to Kay for they effort as a facilitator of the Code Institute team.
- Great thanks go to [Dajana Isbaner](https://github.com/queenisabaer) for being the best fellow student I could wish for.
