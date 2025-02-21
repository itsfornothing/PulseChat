PulseChat: Django Real-Time Chat Application

Overview

This is a real-time chat application built using Django and Django Channels. The project supports one-on-one messaging and group chat functionality, allowing users to communicate in real-time using WebSockets.

Features

User Authentication: Register, login, and logout functionality.

One-on-One Chat: Users can send and receive private messages.

Group Chat: Users can create, join, and chat in groups.

WebSockets for Real-Time Messaging: Messages are instantly updated without refreshing the page.

Online Status Indicators: Shows if a user is online.

Secure Authentication: Uses Django's built-in authentication system.

Database Storage: Chats and user details are stored using SQLite (or PostgreSQL in production).

Dynamic UI Updates: Messages and user statuses update dynamically using WebSockets.

Technologies Used

Backend: Django, Django Channels, WebSockets

Frontend: HTML, CSS, JavaScript, Django Templates

Database: SQLite (default) / PostgreSQL (recommended for production)

WebSocket Handling: Django Channels & ASGI

Installation Guide

1. Clone the Repository

https://github.com/yourusername/chat-app.git
cd chat-app

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Run Migrations

python manage.py migrate

5. Create a Superuser (For Admin Access)

python manage.py createsuperuser

6. Run the Development Server

python manage.py runserver

7. Access the Application

Open your browser and go to:

http://127.0.0.1:8000/

Usage

Register/Login: Create an account or log in with an existing user.

One-on-One Chat: Click on a user to start chatting.

Group Chat: Create a group, invite members, and start messaging.

Real-Time Updates: Messages appear instantly without refreshing the page.

Project Structure

chat-app/
│── files/
│── templates/         # HTML Templates
│── static/            # CSS & JavaScript Files
│── media/             # Uploaded Files
│── chat/              # Chat App Logic
│── pulsechatusers/    # User Model & Authentication
│── consumers.py       # WebSocket Handling
│── views.py           # Django Views
│── urls.py            # URL Routing
│── settings.py        # Django Project Settings
│── manage.py          # Django Management Script

Future Enhancements

Add message notifications

Implement message reactions (emojis)

Improve UI with TailwindCSS or Bootstrap

Add video/audio call functionality

Contributing

Contributions are welcome! Fork this repository, create a new branch, and submit a pull request.
