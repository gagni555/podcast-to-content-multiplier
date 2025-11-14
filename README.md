# Podcast-to-Content Multiplier

> Transform one podcast episode into 10+ content assets in minutes, not hours.

An AI-powered platform that automatically converts podcast audio into blog posts, social media threads, quote graphics, email newsletters, and SEO-optimized show notes—all while maintaining your unique brand voice.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

#### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/podcast-multiplier.git
cd podcast-multiplier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env

# Run database migrations
alembic upgrade head

# Start the API server
python start_server.py
```

Access the application at `http://localhost:8000`

## 📦 Project Structure

```
podcast-multiplier/
├── api/                    # API layer
│   ├── main.py             # Main application entry point
│   ├── database.py         # Database configuration
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── routers/            # API routes
│   └── utils/              # Utility functions
├── alembic/               # Database migration files
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── alembic.ini           # Alembic configuration
├── start_server.py       # Server startup script
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api --cov-report=html
```

## 🏗️ Architecture

The application follows a modern, scalable architecture:

- **FastAPI**: Web framework with automatic API documentation
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database for structured data
- **Redis**: Caching and background job queue
- **Celery**: Background task processing (to be implemented)
- **AWS S3**: File storage for audio and generated assets

## 🔐 Authentication

The application uses JWT tokens for authentication. Register a user first, then use the login endpoint to get an access token.

## 📡 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.