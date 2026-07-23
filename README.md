# 🚀 AI Knowledge Services

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.116+-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/PostgreSQL-17-blue?style=for-the-badge&logo=postgresql" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge&logo=sqlalchemy" />
  <img src="https://img.shields.io/badge/Alembic-Migrations-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenAI-AI-black?style=for-the-badge&logo=openai" />
</p>

<p align="center">
A production-ready AI-powered Knowledge Base service built with <b>FastAPI</b>, <b>PostgreSQL</b>, and <b>OpenAI</b>. Upload PDF documents, manage media, extract information, and ask AI questions using your uploaded knowledge.
</p>

---

# 📖 Overview

AI Knowledge Services is a RESTful backend service that allows users to upload PDF documents, manage media files, extract document content, and query the uploaded knowledge using AI.

The application is designed with a clean Service–Repository architecture, asynchronous database operations, and production-ready FastAPI practices.

---

# ✨ Features

- 📄 Upload PDF documents
- 🗂 Store document metadata
- 🧠 AI-powered question answering
- 🔍 Search uploaded knowledge
- 🎵 Upload audio/video media
- 📝 Update media metadata
- ❌ Delete media
- 📊 Retrieve media information
- 📁 File management
- 🗃 PostgreSQL database
- ⚡ Async SQLAlchemy
- 🔄 Alembic migrations
- 📚 Automatic Swagger Documentation
- ✅ Pydantic validation
- 🛡 Proper HTTP status codes
- 🧩 Modular project architecture

---

# 🏗 Architecture

```
                Client
                   │
                   ▼
             FastAPI Routes
                   │
                   ▼
             Service Layer
                   │
                   ▼
           Repository Layer
                   │
                   ▼
            PostgreSQL Database
                   │
                   ▼
               OpenAI API
```

---

# 📂 Project Structure

```
AI_Knowledge_Services
│
├── alembic/
│
├── app/
│   ├── database/
│   ├── helpers/
│   ├── models/
│   ├── repository/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   ├── config.py
│   ├── main.py
│   └── dependencies.py
│
├── uploads/
│
├── tests/
│
├── .env
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# 🛠 Tech Stack

| Technology | Usage |
|------------|-------|
| FastAPI | REST API |
| Python | Backend |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database Migration |
| OpenAI API | AI Integration |
| Pydantic | Validation |
| Uvicorn | ASGI Server |

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/MalharBhatt-whitelotus/AI_Knowledge_Services.git

cd AI_Knowledge_Services
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file.

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/database_name

OPENAI_API_KEY=your_api_key

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 🗄 Database Migration

Generate Migration

```bash
alembic revision --autogenerate -m "Initial Migration"
```

Run Migration

```bash
alembic upgrade head
```

Rollback

```bash
alembic downgrade -1
```

---

# ▶ Running the Project

```bash
uvicorn app.main:app --reload
```

Application

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# 📌 API Endpoints

## File APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /file/upload | Upload PDF |
| GET | /file/get_all | Get all files |
| GET | /file/{id} | Get file |
| DELETE | /file/delete/{id} | Delete file |

---

## Media APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /media/upload | Upload media |
| GET | /media/get_all_details | Get media |
| PATCH | /media/update/{id} | Update media |
| DELETE | /media/delete/{id} | Delete media |

---

## AI APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /ai/ask | Ask AI question |
| POST | /ai/summarize | Generate summary |

---

# 📤 Example Upload Request

```http
POST /file/upload
```

Form Data

```
file_name = Python Guide

file = python.pdf
```

---

# 📥 Example Response

```json
{
    "id": 1,
    "file_name": "Python Guide",
    "uploaded_at": "2026-07-23T10:20:35"
}
```

---

# 🤖 AI Query Example

Request

```json
{
    "query":"Explain dependency injection."
}
```

Response

```json
{
    "answer":"Dependency Injection is a software design pattern..."
}
```

---

# 🚦 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

# 🧪 Running Tests

```bash
pytest
```

Coverage

```bash
pytest --cov=app
```

---

# 🔒 Security

- Input Validation
- Pydantic Models
- SQL Injection Protection
- Async Database Sessions
- Proper Exception Handling
- Secure File Validation
- MIME Type Verification

---

# 🚀 Future Improvements

- JWT Authentication
- User Roles
- Vector Database
- Semantic Search
- OCR Support
- Image Processing
- Background Tasks
- Redis Cache
- Docker Support
- Kubernetes Deployment
- CI/CD Pipeline
- Rate Limiting

---

# 🤝 Contributing

1. Fork the repository

2. Create your feature branch

```bash
git checkout -b feature/my-feature
```

3. Commit changes

```bash
git commit -m "Feat: Add new feature"
```

4. Push branch

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Malhar Bhatt**

GitHub

https://github.com/MalharBhatt-whitelotus

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository

🍴 Fork the repository

🐛 Report issues

💡 Suggest improvements

---

<p align="center">
Built with ❤️ using FastAPI, PostgreSQL, SQLAlchemy, and OpenAI
</p>