# Factorio Blueprint Library

The Factorio Blueprint Library is a web application that allows users to generate, manage, and share blueprints for the
game Factorio. This project is built using Django and provides a user-friendly interface to interact with blueprints.

## Check it out

[Factorio Blueprint Library project deployed to Render](https://factorio-blueprint-library.onrender.com/)

## Test User Information

For testing purposes, there is a pre-registered user in the system. However, to prevent accidental deletion or
modification of this test user, **it is strongly recommended to register your own test account**. This will ensure that
the default test user remains intact for other developers or future testing.

### Test User Credentials

- **Username**: testuser
- **Password**: testpassword123

**Please do not delete or modify this user.**  
If you need to perform tests that might alter the user state or test with different permissions, create your own test
account via the registration page.

## Installation

To set up this project, ensure you have Python 3 installed on your system. Then, follow these commands:

1. **Clone the Repository**  
   Clone the project repository from GitHub to your local machine.\
   ```git clone https://github.com/OttoLindholm/factorio-blueprint-library.git```
2. **Change Directory**  
   Navigate into the project directory.\
   ```cd factorio-blueprint-library```
3. **Create a Virtual Environment**  
   Create a virtual environment to isolate your project dependencies.
   ```python -m venv venv```
4. **Activate the Virtual Environment**
    - Activate the virtual environment for Windows systems.\
      ```.venv\Scripts\activate # on Windows```
    - Activate the virtual environment for macOS or Linux systems.\
      ```source venv/bin/activate # on macOS```
5. **Install Dependencies**  
   Install the required packages specified in the `requirements.txt` file.\
   ```pip install -r requirements.txt```
6. **Apply Migrations**  
   Apply the migrations to your database to create the necessary tables.\
   ```python manage.py migrate```
7. **Load Demo Data**  
   Load sample data into the database from the provided JSON file.\
   ```python manage.py loaddata demo_data.json```
8. **Run the Development Server**  
   Start the Django development server to run your application locally.\
   ```python manage.py runserver```

## Usage

Once the server is running, you can access the application by navigating to `http://127.0.0.1:8000/` in your web
browser. From there, you can create, view, and manage your Factorio blueprints.

## Demo

![Website Interface](demo.png)

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes.
