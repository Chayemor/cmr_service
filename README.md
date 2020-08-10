Description
====================

REST API to manage customer data for a small shop. It will work as the backend side for a CRM interface. 

API requirements:

- The user API should be only accessible by a registered user by providing an authentication mechanism. 
- The customer API should only be accessible by a user that holds a valid OAUTH2 token
- A user with a valid OAUTH2 token can only:
  - List all customers in the database
  - Get full customer information, including a photo URL
  - Create a new customer
  - A customer should have at least name, surname, id and a photo field
  - Name, surname and id are required fields
  - Image uploads should be able to be managed
  - The customer should have a reference to the user who created it
  - Update an existing customer
  - The customer should hold a reference to the last user who modified it
  - Delete an existing customer
- An admin can do all that users can, and also:
  - Manage users
  - Create users
  - Delete users
  - Update users
  - List users
  - Change admin status


Usage
============================

Installation
----------------

This project was created with docker, to learn more about docker: https://www.docker.com/get-started You should
have little problem starting it up in whatever environment you code in. 

```bash
cd yourProjectFolder
git clone https://github.com/Chayemor/cmr_service.git
```

With this step done you have successfully cloned the repo. Now before running with docker-compose it's 
important to set up the .env variables that docker needs.

Set up
-----------------

There's a file with the name .env_template, copy the file and rename to .env and fill out with desired 
data or leave example data. It's the names of the variables in there that are important, the actual values you write are not.

```bash
cd cmr_service
cp .env_template .env
```

The variable names are self explanatory to their function. I will only mention these ones:

**DJANGO_SU_NAME**
**DJANGO_SU_PASSWORD**

You should remember the values you place for these since this is your admin user. It is the only
user that will be created in the DB once you run the project for the first time. It's your access to create new
Users and set their status to admin. 

Also, if you feel like playing with the code, it's best then to set the .env variable
**APP_ENV** to "dev" (without double quotes). By default, .env_template has that value set to dev, then
if an error occurs, you will get more information about it. You can just as easily set it to prod. 

Run
-----------------

Assuming you are in the repository folder, all that's left to do is build the docker container, then run it.
Note: You must be running Python 3 when you do the docker commands.
 
```bash
docker-compose build
docker-compose up
```

That's it. The API should now be available at **localhost:8000/api/v1/docs**

When you open the browser and go to that route you will see the public API available thanks to the Swagger module. There's 
a current bug in that module that doesn't let the users add the OAUTH2 token when making requests on the Customer api, 
all requests through Swagger have been turned off. For more information: https://github.com/marcgibbons/django-rest-swagger/issues/759 

You must be logged in to view the API, to do so click on the "login" button on the top right. Login with what value is in your .env file for DJANGO_SU_NAME and DJANGO_SU_PASSWORD
This is session based authentication to gain access to the API. The OAUTH2 authentication is used to authorize operation on the Customer's API. Without the OAUTH2 token 
Users won't be able to operate on Customers API.

Once logged in, you will have access to the API and you will be able to create both Users and Customers because your DJANGO_SU_NAME user is an admin. 
You can try creating a user without admin privileges, login out, and then log back in with the created user's credential. You'll see then that the documentation should only show the API endpoints for
customer CRUD operations.

Getting an OAUTH2 Token
============================

Getting the OAUTH2 application (client id and client secret)
-----------------------
Go to the following url: `http://localhost:8000/o/applications/1/` , here you can create an application with the following:

- Name: just a name of your choice
- Client Type: confidential
- Authorization Grant Type: Resource owner password-based

Once saved, remember the **client_id** and **client_secret** , you will need it for the next step.

Getting the OAUTH2 Token
-----------------------
To get the OAUTH2 Token you have to do a QUERY to the following endpoint:

```bash
curl -X POST -d "grant_type=password&username=<user_name>&password=<password_here>" -u"<client_id>:<client_secret>" http://localhost:8000/o/token/
```

You should see a response like this:

```bash
{
 "access_token": "RX6EyFUBlQc2MVqKdVzb0GjiCjkWkU", 
 "expires_in": 36000, 
 "token_type": "Bearer", 
 "scope": "read write groups", 
 "refresh_token": "Ns5lZN4namyos2afIGJltx3wnLYgrq"
 }
```

Now with that **access_token** you can carry out API requests by adding the header, such that:

`curl -H "Authorization: Bearer RX6EyFUBlQc2MVqKdVzb0GjiCjkWkU" http://localhost:8000/api/v1/customers/`

Running Tests
============================

To run tests you must be inside the running container labeled **cmr_service**. 
To log into the docker container take a look at **Common Docker commands --> Log into a docker container**.

To run this command you must be at the same level as **manage.py**, which is the path that you sign into
when you log into the container.

```bash
python manage.py test the_app_name.route.to.test.file
```

```bash
python manage.py test users.tests.tests
```

You should look for the following output:

```bash
root@115f46c7f03e:/django-docker# python manage.py test users.tests.tests
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 12.621s

OK
Destroying test database for alias 'default'...
```

Search for the **OK** which means all tests have passed. You can find the numerous test over
at each app's directory under tests.

Common Docker commands
============================

## View running containers 

```bash
docker ps
```
```bash 
CONTAINER ID        IMAGE                            COMMAND                  CREATED             STATUS              PORTS                    NAMES
115f46c7f03e        cmr_service_web                  "bash /entrypoint.sh"    2 hours ago         Up 2 hours          0.0.0.0:8000->8000/tcp   cmr_service
603f6d1c9db7        postgres:9.6                     "docker-entrypoint.s…"   4 days ago          Up 2 hours          0.0.0.0:5432->5432/tcp   cmr_service_postgres_1
```

You should get something like this. The last column, **NAMES** are the names of the running containers. If you ever want to log into one, you need that name. The 
**cmr_service** contains the actual code for the API, while the **cmr_service_postgres_1** is the container that holds the database itself. If you want to be
able to log into Postgres, you'd log into that container, and not **cmr_service**.

## Log into a docker container

```bash
docker exec -it docker_container_name bash
```

Example: **cmr_service**

```bash
docker exec -it cmr_service bash
```

Once logged in, if you do a simple ```ls``` you'd see the following:

```bash
root@115f46c7f03e:/django-docker# ls
Dockerfile  README.md  cmr_service  customers  db_init	docker-compose.yml  entrypoint-dev.sh  entrypoint-prod.sh  manage.py  media  requirements  users  wait-for-it.sh
```

## Start a container without a rebuild
Assuming you are in the same path as the root repo.

```bash
docker-compose up
```

## Force build of a container 
Assuming you are in the same path as the root repo.

```bash
docker-compose build --no-cache
```

## Kill everything
Something has gone awfully wrong and you need to do a mission abort, obliterating all
containers and images. Proceed with caution.

```bash
docker system prune
```

Things to improve
============================
- More tests
- Check photo size before saving, could easily load a big file and use up all disk space
- OAuth2
