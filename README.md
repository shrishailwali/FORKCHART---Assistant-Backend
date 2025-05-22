<h1 align="center">🤖 FORKCHART – Assistant Backend</h1> <p align="center"> A modular and scalable <strong>FastAPI</strong> backend built for intelligent AI-powered assistants.<br/> Supports user account management, real-time chat, and seamless MongoDB integration. </p> <p align="center"> <img src="https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python" /> <img src="https://img.shields.io/badge/FastAPI-🚀-green?style=flat&logo=fastapi" /> <img src="https://img.shields.io/badge/MongoDB-🧩-brightgreen?style=flat&logo=mongodb" /> <img src="https://img.shields.io/badge/uv-Fast%20Installer-yellow?style=flat" /> </p>

🔥 Key Features
🔐 User Account Module
Easily manage user registration, login, and profile operations with clean schema and service layers.

💬 AI Chat Module
Integrate conversational AI using a powerful, pluggable architecture to support various AI providers.

⚙️ Clean Modular Architecture
Follows separation of concerns across models, schemas, views, and services for scalability and maintenance.

🧩 MongoDB Support
Utilizes pymongo for fast, scalable document-based storage.

⚡ Powered by FastAPI
High-performance web framework with automatic interactive docs and async support.

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

![alt text]({94A0316C-4F33-4E9B-8337-8BB13EC27761}.png)