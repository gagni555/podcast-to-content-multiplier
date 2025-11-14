# Codebase Infrastructure

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web App    │  │  Mobile API  │  │  CLI Tool    │          │
│  │  (React)     │  │  (GraphQL)   │  │  (Python)    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                    ┌────────▼────────┐
                    │   API Gateway   │
                    │   (FastAPI)     │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────▼────────┐ ┌───────▼────────┐ ┌──────▼─────────┐
│  Auth Service    │ │  Job Queue     │ │  WebSocket     │
│  (OAuth2/JWT)    │ │  (Celery)      │ │  (Socket.io)   │
└─────────┬────────┘ └───────┬────────┘ └──────┬─────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Core Processor   │
                    │  Orchestrator     │
                    └────────┬──────────┘
                             │
          ┌──────────────────┼──────────────────────┐
          │                  │                      │
┌─────────▼────────┐ ┌───────▼────────┐ ┌──────────▼─────────┐
│  Audio Pipeline  │ │  AI Engine     │ │  Output Generator  │
│  - Upload        │ │  - LLM Agents  │ │  - Templates       │
│  - Validation    │ │  - Embeddings  │ │  - Formatters      │
│  - Transcription │ │  - RAG Chain   │ │  - Assets          │
└─────────┬────────┘ └───────┬────────┘ └──────────┬─────────┘
          │                  │                      │
          └──────────────────┼──────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Data Layer       │
                    │  - PostgreSQL     │
                    │  - Redis Cache    │
                    │  - S3 Storage     │
                    │  - Vector DB      │
                    └───────────────────┘
```

## Component Architecture

### 1. Audio Processing Pipeline

**Purpose**: Handle audio ingestion, validation, and transcription

```
AudioUpload → Validation → Storage → Transcription → Diarization
                                ↓
                          Preprocessing
                                ↓
                    [Feature Extraction]
                     - Segments
                     - Timestamps
                     - Speaker IDs
                     - Audio quality metrics
```

**Key Modules**:
- `audio_validator.py`: Format checking, duration limits, quality assessment
- `transcription_service.py`: Integrates with Whisper API or AssemblyAI
- `diarization_engine.py`: Speaker identification and separation
- `audio_processor.py`: Waveform analysis, silence detection, chapter marks

### 2. AI Engine Architecture

**Purpose**: Content understanding, extraction, and generation

```
Transcript Input
      ↓
[Semantic Analysis]
      ↓
   ┌──┴──────────────────┬────────────────┬──────────────┐
   ↓                     ↓                ↓              ↓
Topic                 Key             Sentiment      Entity
Extraction          Moments          Analysis      Recognition
   ↓                     ↓                ↓              ↓
   └──┬──────────────────┴────────────────┴──────────────┘
      ↓
[Content Graph Construction]
      ↓
   ┌──┴───────────────┬──────────────────┬────────────┐
   ↓                  ↓                  ↓            ↓
Blog Post          Social            Quote        Newsletter
Generator         Threads           Cards         Composer
   ↓                  ↓                  ↓            ↓
Output Queue    Output Queue     Output Queue   Output Queue
```

**Agent System**:

1. **Coordinator Agent** (`agents/coordinator.py`)
   - Orchestrates multi-step workflow
   - Routes tasks to specialized agents
   - Manages context and state

2. **Content Analyzer Agent** (`agents/analyzer.py`)
   - Extracts topics, themes, and structure
   - Identifies quotable moments
   - Maps content graph

3. **Writer Agents** (`agents/writers/`)
   - `blog_writer.py`: Long-form content generation
   - `social_writer.py`: Platform-specific threads
   - `newsletter_writer.py`: Email-optimized content

4. **Quality Assurance Agent** (`agents/qa.py`)
   - Fact-checking against transcript
   - Brand voice compliance
   - SEO optimization validation

### 3. Content Generation Flow

```python
# Pseudocode representation
class ContentOrchestrator:
    def process_episode(self, audio_file, user_config):
        # Step 1: Audio Processing
        transcript = self.audio_pipeline.transcribe(audio_file)
        segments = self.audio_pipeline.segment(transcript)
        
        # Step 2: Semantic Understanding
        context = self.ai_engine.analyze(transcript, segments)
        content_graph = self.ai_engine.build_graph(context)
        
        # Step 3: Parallel Generation
        tasks = [
            self.generate_blog(content_graph, user_config),
            self.generate_social(content_graph, user_config),
            self.generate_newsletter(content_graph, user_config),
            self.generate_graphics(content_graph, user_config)
        ]
        results = await asyncio.gather(*tasks)
        
        # Step 4: Quality Check
        validated = self.qa_agent.validate(results, transcript)
        
        # Step 5: Asset Packaging
        return self.packager.bundle(validated, user_config)
```

### 4. Database Schema

**PostgreSQL Tables**:

```sql
-- Users & Authentication
users (id, email, auth_provider, subscription_tier, brand_config)
sessions (id, user_id, token, expires_at)

-- Episodes & Processing
episodes (id, user_id, audio_url, title, duration, status, created_at)
transcripts (id, episode_id, text, segments_json, speakers_json)
processing_jobs (id, episode_id, job_type, status, progress, error_log)

-- Generated Content
blog_posts (id, episode_id, title, content, seo_metadata, status)
social_threads (id, episode_id, platform, thread_json, scheduled_at)
newsletters (id, episode_id, subject, html_content, plain_text, variant)
quote_cards (id, episode_id, quote_text, image_url, design_config)

-- Analytics
content_performance (id, content_id, content_type, views, clicks, shares)
user_analytics (id, user_id, episodes_processed, time_saved, satisfaction)
```

**Redis Cache Structure**:
```
user_session:{user_id} → session data
job_status:{job_id} → processing progress
rate_limit:{user_id}:{endpoint} → API throttling
brand_config:{user_id} → cached brand settings
```

**Vector Database** (Pinecone/Weaviate):
```
embeddings:{episode_id}:chunks → semantic search
embeddings:{user_id}:voice_profile → brand voice consistency
```

### 5. API Architecture

**REST Endpoints** (FastAPI):

```
POST   /api/v1/episodes/upload        # Upload audio file
GET    /api/v1/episodes/{id}          # Get episode details
POST   /api/v1/episodes/{id}/process  # Start content generation
GET    /api/v1/episodes/{id}/outputs  # List generated content
GET    /api/v1/blog/{id}              # Retrieve blog post
POST   /api/v1/social/schedule        # Schedule social posts
GET    /api/v1/analytics/dashboard    # User analytics
```

**WebSocket Channels**:
```
ws://api/v1/jobs/{job_id}  # Real-time progress updates
```

### 6. Modular Structure

```
podcast-multiplier/
│
├── api/                          # API layer
│   ├── routes/                   # Endpoint definitions
│   ├── middleware/               # Auth, CORS, rate limiting
│   └── schemas/                  # Pydantic models
│
├── core/                         # Business logic
│   ├── orchestrator.py           # Main workflow coordinator
│   ├── audio_pipeline/           # Audio processing modules
│   ├── ai_engine/                # AI agents and processors
│   └── content_generators/       # Format-specific generators
│
├── agents/                       # Agentic AI system
│   ├── coordinator.py            # Master agent
│   ├── analyzer.py               # Content analysis
│   ├── writers/                  # Specialized writer agents
│   └── qa.py                     # Quality assurance
│
├── services/                     # External integrations
│   ├── transcription/            # Whisper, AssemblyAI
│   ├── llm/                      # OpenAI, Anthropic, local models
│   ├── storage/                  # S3, CDN
│   └── publishing/               # CMS, social platforms
│
├── models/                       # Database models (SQLAlchemy)
├── utils/                        # Helpers and utilities
├── workers/                      # Celery background tasks
└── tests/                        # Test suites
```

### 7. Deployment Architecture

**Development Environment**:
```
Docker Compose Stack:
- API (FastAPI)
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat (scheduler)
- Nginx (reverse proxy)
```

**Production Environment**:
```
- API: AWS ECS / Kubernetes pods
- Database: AWS RDS PostgreSQL
- Cache: AWS ElastiCache Redis
- Storage: S3 + CloudFront CDN
- Queue: AWS SQS + Lambda workers
- Monitoring: DataDog / Prometheus + Grafana
```

### 8. Data Flow Example

```
1. User uploads podcast.mp3 (45 mins)
   → Stored in S3
   → Job created with ID: job_abc123
   
2. Transcription worker picks up job
   → Sends to Whisper API
   → Returns transcript in 2-3 minutes
   → Stores in DB with timestamps
   
3. AI Coordinator agent receives transcript
   → Analyzes: 5 main topics, 12 key quotes, 3 speakers
   → Builds content graph
   
4. Parallel generation (3-4 minutes):
   → Blog Writer: 2000-word SEO post
   → Social Writer: 10-tweet thread + 5 LinkedIn posts
   → Newsletter Writer: 500-word summary + CTA
   → Quote Designer: 8 branded graphics
   
5. QA Agent validates (30 seconds):
   → Checks facts against transcript
   → Validates brand voice
   → Scores readability
   
6. Content packaged and stored
   → User receives notification
   → Dashboard shows all outputs
   → Ready for publishing

Total time: ~6-8 minutes
```

## Scalability Considerations

- **Horizontal Scaling**: Stateless API design allows unlimited container scaling
- **Async Processing**: Celery workers handle long-running tasks independently
- **Caching Strategy**: Redis reduces database load for repeated queries
- **CDN Distribution**: Static assets (images, audio) served via CloudFront
- **Database Optimization**: Indexed queries, connection pooling, read replicas

---

**Architecture Version**: 2.1  
**Last Updated**: November 2025