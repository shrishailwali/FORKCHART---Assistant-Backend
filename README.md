🚀 FORKCHART – Assistant Backend
A modular and scalable FastAPI backend for an AI Assistant application. Built with clean architecture principles, it provides user account management, AI-powered chat capabilities, and seamless MongoDB integration.

✨ Features
🔐 User Account Module
Manage users with robust models, schemas, and API endpoints.

💬 Chat Module
AI-driven chat functionality for intelligent user interaction.

⚙️ Modular Architecture
Clean separation of concerns: models, schemas, views, and services.

🧩 MongoDB Integration
Efficient and scalable NoSQL database support using pymongo.

⚡ FastAPI Framework
Fast, modern, and intuitive Python web framework.

📦 uv Package Manager
Ultra-fast Python package installer for seamless dependency management.

📦 Requirements
Python 3.11+
FastAPI
pymongo
postgresql
bcrypt, etc
uv (Python package manager)

🛠️ Installation
Clone the repository and navigate into the project directory:


git clone https://github.com/shrishailwali/FORKCHART---Assistant-Backend.git
cd FORKCHART---Assistant-Backend/new

⚙️ Configuration
Configure your environment settings in the config.py file:


MongoDB:

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "your_database_name"

Postgresql DB:
SQLALCHEMY_DATABASE = "postgresql://postgres:postgres@localhost:5432/forkchat"
# Add any additional environment configs here


🧪 Running the Application
Start the FastAPI server using uv:
uv run run.py

Once the server is running, explore the interactive API documentation at:
👉 http://127.0.0.1:8000/docs