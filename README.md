# Podcast-to-Content Multiplier

> Transform one podcast episode into 10+ content assets in minutes, not hours.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://react.dev)

An AI-powered platform that automatically converts podcast audio into blog posts, social media threads, quote graphics, email newsletters, and SEO-optimized show notes—all while maintaining your unique brand voice.

---

## 🎯 Features

### Content Generation
- **Blog Posts**: SEO-optimized 1500-2500 word articles with proper structure
- **Social Threads**: Platform-specific content for Twitter/X, LinkedIn, Instagram
- **Quote Graphics**: Branded visual cards with audiogram snippets
- **Newsletters**: Email-ready content with CTAs and segmentation
- **Show Notes**: Searchable notes with timestamps and key topics

### AI-Powered Intelligence
- Speaker diarization and identification
- Topic extraction and key moment detection
- Sentiment analysis for quote selection
- Brand voice cloning for consistency

### Workflow Automation
- One-click processing from upload to publish
- Direct CMS integration (WordPress, Medium, Ghost)
- Social media scheduling
- Real-time analytics dashboard

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional, recommended)

### Installation

#### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/podcast-multiplier.git
cd podcast-multiplier

# Copy environment variables
cp .env.example .env

# Edit .env with your API keys
nano .env

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec api alembic upgrade head

# Create a superuser
docker-compose exec api python scripts/create_user.py
```

Access the application at `http://localhost:3000`

#### Manual Setup

**Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload --port 8000
```

**Frontend Setup**

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Background Workers**

```bash
# In a new terminal, start Celery worker
cd backend
celery -A app.workers.celery_app worker --loglevel=info

# In another terminal, start Celery beat (scheduler)
celery -A app.workers.celery_app beat --loglevel=info
```

---

## 📖 Usage

### Basic Workflow

1. **Upload your podcast audio**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/episodes/upload" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "file=@podcast.mp3" \
     -F "title=Episode 42: Remote Work Tips"
   ```

2. **Start content generation**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/episodes/{episode_id}/process" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"formats": ["blog", "social", "newsletter", "graphics"]}'
   ```

3. **Monitor progress via WebSocket**
   ```javascript
   const socket = io('http://localhost:8000');
   socket.on(`job:${jobId}:progress`, (data) => {
     console.log(`Progress: ${data.progress_percent}%`);
   });
   ```

4. **Retrieve generated content**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/episodes/{episode_id}/outputs" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Python SDK

```python
from podcast_multiplier import PodcastMultiplier

# Initialize client
client = PodcastMultiplier(api_key="your_api_key")

# Upload and process
episode = client.episodes.create(
    audio_file="episode.mp3",
    title="My Awesome Episode",
    formats=["blog", "social", "newsletter"]
)

# Wait for completion
episode.wait_for_completion()

# Get blog post
blog = episode.get_blog_post()
print(blog.content)

# Publish to WordPress
blog.publish_to_wordpress(
    site_url="https://myblog.com",
    username="admin",
    password="app_password"
)
```

### JavaScript/TypeScript SDK

```typescript
import { PodcastMultiplier } from '@podcast-multiplier/sdk';

const client = new PodcastMultiplier({ apiKey: 'your_api_key' });

// Upload and process
const episode = await client.episodes.create({
  audioFile: file,
  title: 'My Awesome Episode',
  formats: ['blog', 'social', 'newsletter'],
});

// Listen for progress
episode.on('progress', (data) => {
  console.log(`${data.stage}: ${data.progress}%`);
});

// Get results
const blog = await episode.getBlogPost();
const social = await episode.getSocialThreads();
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
ASSEMBLYAI_API_KEY=...

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/podcast_multiplier
REDIS_URL=redis://localhost:6379/0

# Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET_NAME=podcast-audio-files

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Processing
MAX_AUDIO_DURATION_SECONDS=14400
MAX_FILE_SIZE_MB=500
DEFAULT_BLOG_LENGTH=2000
```

### Brand Configuration

Create a `brand.yaml` file:

```yaml
brand:
  name: "My Podcast"
  
  voice:
    tone: "professional yet conversational"
    style: "storytelling with data"
    perspective: "first-person"
    humor_level: "moderate"
    
  visual:
    logo_url: "https://example.com/logo.png"
    primary_color: "#3B82F6"
    secondary_color: "#10B981"
    font_heading: "Inter"
    font_body: "Source Sans Pro"
    
  content:
    cta_default: "Subscribe for more insights"
    hashtags: ["#podcast", "#productivity"]
    target_keywords: ["remote work", "productivity"]
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_content_generation.py

# Run frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

---

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Create new user account |
| POST | `/api/v1/auth/login` | Authenticate and get token |
| POST | `/api/v1/episodes/upload` | Upload audio file |
| POST | `/api/v1/episodes/{id}/process` | Start content generation |
| GET | `/api/v1/episodes/{id}` | Get episode details |
| GET | `/api/v1/episodes/{id}/outputs` | List generated content |
| GET | `/api/v1/blog/{id}` | Get blog post |
| GET | `/api/v1/social/{id}` | Get social threads |
| POST | `/api/v1/social/schedule` | Schedule social posts |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                           │
│  Web App (React) │ Mobile API │ CLI Tool                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │   API Gateway   │ FastAPI
         │   (FastAPI)     │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼────┐  ┌────▼─────┐
│  Auth  │  │  Queue  │  │ WebSocket│
│Service │  │ (Celery)│  │          │
└───┬────┘  └────┬────┘  └────┬─────┘
    │            │            │
    └────────────┼────────────┘
                 │
        ┌────────▼─────────┐
        │  Core Processor  │
        │  Orchestrator    │
        └────────┬──────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼─────┐ ┌───▼────┐ ┌────▼──────┐
│  Audio  │ │   AI   │ │  Output   │
│Pipeline │ │ Engine │ │ Generator │
└────┬────┘ └───┬────┘ └────┬──────┘
     │          │          │
     └──────────┼──────────┘
                │
       ┌────────▼─────────┐
       │   Data Layer     │
       │ PostgreSQL+Redis │
       └──────────────────┘
```

See [codebase-infrastructure.md](docs/codebase-infrastructure.md) for detailed architecture.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup

```bash
# Fork and clone the repo
git clone https://github.com/yourusername/podcast-multiplier.git

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git commit -m "Add amazing feature"

# Push and create a pull request
git push origin feature/amazing-feature
```

### Code Style

- **Python**: Black, Ruff, mypy
- **TypeScript**: ESLint, Prettier
- **Commits**: Conventional Commits format

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com) for the amazing web framework
- [LangChain](https://langchain.com) for AI orchestration tools
- [OpenAI](https://openai.com) and [Anthropic](https://anthropic.com) for LLM APIs
- [AssemblyAI](https://assemblyai.com) for transcription services

---

## 📞 Support

- **Documentation**: [docs.podcastmultiplier.com](https://docs.podcastmultiplier.com)
- **Discord**: [Join our community](https://discord.gg/podcast-multiplier)
- **Email**: support@podcastmultiplier.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/podcast-multiplier/issues)

---

## 🗺️ Roadmap

- [x] Core audio transcription
- [x] Blog post generation
- [x] Social media threads
- [ ] Video podcast support (extract audio)
- [ ] Multi-language support (20+ languages)
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] White-label for agencies
- [ ] Voice cloning for audio snippets
- [ ] Mobile apps (iOS, Android)

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/podcast-multiplier?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/podcast-multiplier?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/podcast-multiplier?style=social)

---

<div align="center">
  <strong>Built with ❤️ by podcast creators, for podcast creators</strong>
  <br />
  <sub>Star this repo if you find it useful!</sub>
</div>