## Applications

### Common

#### Setting Up Applications
Setting up both the application is similar.
Simply follow the following commands.

* **Getting code on your local machine**

    Make sure you have git installed. if not you can download it from the following link.
    
    https://git-scm.com/downloads
    
    * Clone the repository to your local machine. Goto the folder where you want the project 
      to be saved and run the following command.
      ```bash
      git clone https://github.com/vaskrneup/SpeerTechnologiesAPIProjects
      ```
    * You will now see a new folder containing the project files. We will get back to it later.

* **Installing python**
    
    The backend is written in Django(A Web Development Framework for python).
    Lets start by downloading python from the following link.
    Please follow the instructions on the website as per your Operating System.

    https://www.python.org/downloads/

* **Installing Django and other Dependent Packages**

    If you are in Linux based OS please make sure you have pip installed.
    You can follow this link for Linux based OS.
    (https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/).
    
    Goto the project folder and run the following command. 
    
    ```bash
    # installs all the required packages
    pip install -r requirements.txt
    ```
* **Running the Programs**

    The process of running both the project is same. Just cd into the project you want to run.
    ```bash
    cd TwitterAPI
    # OR
    cd StockMarketTracking
    ```
    
    Then run the following commands
    
    ```bash
    # create migrations for the database 
    # [FOR StockMarketTracking]
    python manage.py makemigrations user share_manager wallet 
    # [FOR TwitterAPI]    
    python manage.py makemigrations user tweet
  
    # OTHER COMMANDS ARE THE SAME FOR BOTH PROJECTS
    # apply migrations to the database
    python manage.py migrate
  
    # create a user for testing the APIs and for accessing Admin Panel
    # Follow the instructions after typing the command for creating a new user
    python manage.py createsuperuser
    
    # running the program
    python manage.py runserver
  
    # follow the link displayed in the console.
    ```
  
* **Finding the documentation for APIs, Models and others [MAKE SURE TO CHECK THE PORT, COULD BE DIFFERENT]**
  * APIs Documentation
  
    http://localhost:8000/admin/doc/views/
  
  * Database Models Documentation
  
    http://localhost:8000/admin/doc/models/

  * All Documentation Available
  
    http://localhost:8000/admin/doc/