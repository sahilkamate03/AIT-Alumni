# AIT Connect Project

## Overview
The AIT Connect project is designed to bridge the gap between current students and alumni of the AIT (Army Institute of Technology) institute. It serves as a common platform for interaction, information sharing, and collaboration between students and alumni. The project facilitates communication regarding internship opportunities, career guidance, updates on current happenings at AIT, and more.

## Getting Started

1. Visit the [link](https://ait-alumini.sahilkamate.repl.co/login).
2. Enter the credentials.

        Credentials
        Email: sahilkamate_21185@aitpune.edu.in
        Password: 123456
3. Explore the site.
### Local Setup
To run the project locally, follow these steps:

1. Clone the repository.
2. Install the necessary dependencies.
3. Configure Firebase credentials.
4. Run the Flask application.

## Technical Details

### Technologies Used
- **Python**: The backend of the project is implemented using Python.
- **Flask**: Flask is utilized as the web framework for building the backend.
- **Firebase**: Firebase serves as the backend database, ensuring secure and scalable data storage.
- **HTML, CSS, and JS**: The frontend of the project is developed using a simple combination of HTML, CSS, and JavaScript.

### Key Features
1. **User Registration**: Only students and alumni with AIT email addresses can register on the platform.
2. **Alumni Posting**: Alumni have the exclusive privilege to post on the website, sharing valuable insights and information.
3. **Chat Section**: A real-time chat section is implemented using web sockets, enabling communication between alumni and students.
4. **Follow System**: Users can follow alumni to receive updates and posts from specific individuals.
5. **Post Filtering**: Posts can be filtered based on criteria such as top posts and most liked posts.
6. **Security**: The project prioritizes security by utilizing Firebase as the backend, ensuring a robust and secure platform.
7. **Organized Structure**: The project maintains a proper folder structure, with well-named functions and files for clarity and maintainability.


## Folder Structure

 ### Flask Blueprints for Folder Structure
The project leverages Flask Blueprints to maintain a clean and organized folder structure. This helps in modularizing the application, making it more scalable and maintainable. Here is a breakdown of the folder structure:

    /ait
        |-- static
        |-- templates
        |-- views
        |-- __init__.py
        |-- forms.py
        |-- models.py
    |-- app.py
    |-- requirements.txt
    |-- README
 


## Dependencies
- Flask
- Firebase SDK
- [Other dependencies listed in requirements.txt]

## Screenshots

Dashboard

![alt Dashboard](https://github.com/sahilkamate03/AIT-Alumni/blob/dev/screenshots/dashboard.png?raw=true)

Profile

![alt Profile](https://github.com/sahilkamate03/AIT-Alumni/blob/dev/screenshots/profile.png?raw=true)

Follow Page

![alt Setting](https://github.com/sahilkamate03/AIT-Alumni/blob/dev/screenshots/follow.png?raw=true)

Chat

![alt Chat](https://github.com/sahilkamate03/AIT-Alumni/blob/dev/screenshots/chat.png?raw=true)


Settings

![alt Setting](https://github.com/sahilkamate03/AIT-Alumni/blob/dev/screenshots/settings.png?raw=true)