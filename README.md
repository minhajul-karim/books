# Books

This is a book review website. Users will be able to register here and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. We will also use a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via this website’s API.

### Let's see what's inside the files.

I've tried to make this application modular. So, I've used the idea of the blueprint. The main app resides in the application folder that has 3 modules.

 1. Auth: This module contains the logics related to user authentication.
 2. Main: This module contains mostly book search and view results logics.
 3. API: As this name suggests this module contains all logics of our API.
 
Two of these modules have their own template directory, though each module shares some common templates and static files.
- Inside our application, there is an __init__.py file which plays a vital role. It puts together all modules and makes a wonderful combination which is very promising but not runnable yet. 
- Outside application we have a config file(e.g. config.py) which contains critical configuration settings required to run this app smoothly.
- What import.py does is, it reads data from books.csv and imports it to our PostgreSQL database.
- We've used Pipenv for a virtual environment so that, Pipfile and Pipfile.lock is required.
- Wsgi.py is the file that puts our app in the track, starts the engine and voilà, it works!

> Written with [StackEdit](https://stackedit.io/).
