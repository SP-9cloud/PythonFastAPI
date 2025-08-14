# 🚀 FastAPI + MongoDB CRUD API with JWT Authentication

This project is a lightweight REST API built with **FastAPI** and **MongoDB**, featuring:

- 🧱 Basic **CRUD operations**
- 🔐 **JWT-based Authentication**
- 🌐 Fast and asynchronous API
- 📦 MongoDB integration via **Motor**

---

## 📂 Features

- **User Registration and Login**
- **JWT Token Authentication**
- **Create, Read, Update, Delete** operations on data
- **MongoDB** for persistent storage
- **Environment Configuration** using `.env`

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Motor](https://motor.readthedocs.io/) – Async MongoDB driver
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/) – JWT tokens
- [Pydantic](https://docs.pydantic.dev/) – Data validation

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8+
- MongoDB running locally or via cloud (MongoDB Atlas)

### 🧪 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fastapi-mongo-crud-jwt.git
cd fastapi-mongo-crud-jwt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
