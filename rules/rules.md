# Rules: AI Agent Operating Guidelines

## Purpose

This document defines the operational rules, constraints, and behavioral guidelines for all AI agents within the Podcast-to-Content Multiplier system. These rules ensure safe, consistent, reliable, and high-quality autonomous code generation, content creation, and system interaction.

---

## 1. Role Definition & Scope

### 1.1 Agent Roles

**Coordinator Agent**
- **Primary Function**: Orchestrate multi-step content generation workflows
- **Scope**: Task routing, context management, error handling, quality validation
- **Constraints**: Cannot modify user data without explicit job request

**Content Analyzer Agent**
- **Primary Function**: Extract semantic meaning, topics, and structure from transcripts
- **Scope**: NLP analysis, entity extraction, sentiment analysis, topic modeling
- **Constraints**: Read-only access to transcripts; cannot generate user-facing content

**Writer Agents** (Blog, Social, Newsletter)
- **Primary Function**: Generate platform-specific content in user's brand voice
- **Scope**: Content creation based on analyzed transcript data
- **Constraints**: Must maintain factual accuracy to transcript; cannot add external claims

**Quality Assurance Agent**
- **Primary Function**: Validate generated content against quality standards
- **Scope**: Fact-checking, brand voice verification, SEO validation, readability scoring
- **Constraints**: Can reject outputs but cannot autonomously regenerate

### 1.2 Authority Boundaries

**Agents MAY**:
- Read transcripts, user preferences, and brand configurations
- Generate content within their specialized domain
- Call other agents via the coordinator
- Log decisions and rationale for debugging
- Request user input for ambiguous situations

**Agents MUST NOT**:
- Access data outside their job scope (no cross-user data access)
- Modify database records directly (must use service layer)
- Make external API calls without rate limit checks
- Execute code in production without safety validation
- Store sensitive data in logs or intermediate files
- Override user brand settings without explicit permission

---

## 2. Reasoning & Decision-Making Protocols

### 2.1 Chain-of-Thought Process

All agents must follow this reasoning pattern:

```
1. UNDERSTAND: Parse input context and requirements
2. PLAN: Break task into logical sub-steps
3. VALIDATE: Check constraints and prerequisites
4. EXECUTE: Perform task with incremental validation
5. VERIFY: Confirm output meets quality standards
6. DOCUMENT: Log decisions and rationale
```

**Example** (Blog Writer Agent):
```
UNDERSTAND: 
- Transcript: 45-min episode about remote work productivity
- Brand voice: Professional but conversational
- Target length: 1800-2000 words

PLAN:
- Extract 5-7 main topics from transcript
- Create outline with H2/H3 structure
- Write introduction with hook
- Develop body sections with examples
- Add conclusion with CTA

VALIDATE:
- User has Pro plan (allows 2000-word posts)
- No restricted keywords in transcript
- Brand voice profile is complete

EXECUTE:
[Generate content section by section]

VERIFY:
- Word count: 1,947 ✓
- Flesch reading score: 65 ✓
- All claims reference transcript ✓
- Brand voice match: 92% ✓

DOCUMENT:
- Processing time: 87 seconds
- LLM calls: 3 (outline, body, polish)
- Confidence score: 0.94
```

### 2.2 Handling Ambiguity

When encountering unclear instructions or missing data:

1. **Attempt Resolution**: Use context clues and defaults
2. **Confidence Check**: If confidence < 70%, escalate
3. **Escalation Path**: 
   - Minor ambiguity → Use safest default + log decision
   - Major ambiguity → Pause job and request user input
   - Critical ambiguity → Abort and notify user with clear explanation

**Example**:
```
Ambiguous: "Make the blog post more engaging"

Resolution:
- Add storytelling elements from transcript
- Include 2-3 relevant examples
- Use active voice throughout
- Add rhetorical questions in introduction
- Confidence: 85% → Proceed with logging
```

### 2.3 Error Recovery

**Graceful Degradation Strategy**:

| Error Type | Agent Response | User Impact |
|------------|----------------|-------------|
| API timeout | Retry 3x with exponential backoff | Slight delay (< 30s) |
| LLM refusal | Try alternative prompt formulation | Transparent to user |
| Invalid transcript | Request re-upload with diagnostics | Requires user action |
| Out of memory | Process in smaller chunks | Slight delay (< 2min) |
| Rate limit hit | Queue and process when available | Delayed completion |

**Never**: Fail silently, return partial outputs without warning, or lose user data

---

## 3. Data Handling & Safety Rules

### 3.1 Data Access Principles

**Principle of Least Privilege**:
- Agents access only data required for their specific task
- Database queries scoped to `user_id` and `job_id`
- No direct access to authentication tokens or payment data

**Data Retention**:
- Intermediate outputs stored for 7 days (debugging)
- Audio files auto-deleted after 90 days (configurable)
- User deletions must cascade to all generated content

### 3.2 Content Safety

**Prohibited Content Detection**:
Agents must refuse to process or generate:
- Hate speech or discriminatory content
- Explicit sexual content or NSFW material
- Instructions for illegal activities
- Medical or legal advice (flag for human review)
- Copyrighted material (music, unauthorized quotes)

**Safety Check Protocol**:
```python
def content_safety_check(text: str) -> SafetyResult:
    """
    Run before generating any user-facing content
    """
    checks = [
        check_hate_speech(text),
        check_violence(text),
        check_sexual_content(text),
        check_legal_medical_claims(text),
    ]
    
    if any(check.is_violation for check in checks):
        return SafetyResult(
            safe=False,
            reason=checks[0].violation_type,
            action="BLOCK_AND_NOTIFY_USER"
        )
    
    return SafetyResult(safe=True)
```

### 3.3 Privacy Protection

**PII Handling**:
- Redact email addresses, phone numbers, addresses from transcripts
- Never include PII in logs or error messages
- Anonymize data in analytics aggregations

**GDPR Compliance**:
- Honor "right to be forgotten" requests within 30 days
- Provide data export in machine-readable format
- Log all data access for audit trails

---

## 4. API & External Service Interaction

### 4.1 Rate Limiting

**Self-Imposed Limits** (prevent account suspension):
```python
RATE_LIMITS = {
    "openai_gpt4": 3500 tokens/min,
    "anthropic_claude": 4000 tokens/min,
    "assemblyai": 100 concurrent jobs,
    "s3_uploads": 1000 requests/sec,
}
```

**Enforcement**:
- Use Redis-based token bucket algorithm
- Queue requests when approaching limits
- Fail fast if queue exceeds 5-minute backlog

### 4.2 API Error Handling

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(APITimeout)
)
async def call_llm_api(prompt: str) -> str:
    """
    Resilient API call with automatic retries
    """
    try:
        response = await llm_client.complete(prompt)
        return response.text
    except APIError as e:
        if e.status_code == 429:  # Rate limit
            await asyncio.sleep(60)  # Wait 1 minute
            raise  # Trigger retry
        elif e.status_code >= 500:  # Server error
            raise  # Trigger retry
        else:
            log_error(e)
            raise  # Don't retry client errors
```

### 4.3 Cost Management

**Budget Enforcement**:
- Track API costs per job in real-time
- Set per-job cost ceiling: $2.00 (configurable by tier)
- Alert user if job exceeds 75% of budget
- Abort if exceeds 100% with clear notification

**Cost Optimization**:
- Use cheaper models for simple tasks (GPT-3.5 for summaries)
- Cache repeated queries (transcript analysis)
- Batch API calls where possible

---

## 5. Code Generation Rules

### 5.1 Coding Standards

**Python Style** (Backend):
- Follow PEP 8 with Black formatting
- Type hints required for all function signatures
- Docstrings for all public functions (Google style)
- Maximum function length: 50 lines
- Maximum file length: 500 lines

```python
async def generate_blog_post(
    transcript: Transcript,
    user_config: BrandConfig,
    target_length: int = 2000
) -> BlogPost:
    """
    Generate SEO-optimized blog post from podcast transcript.
    
    Args:
        transcript: Processed podcast transcript with segments
        user_config: User's brand voice and style settings
        target_length: Desired word count (default: 2000)
    
    Returns:
        BlogPost object with content, metadata, and SEO fields
    
    Raises:
        ContentGenerationError: If LLM fails to generate valid content
        ValidationError: If output doesn't meet quality thresholds
    """
    # Implementation
```

**TypeScript Style** (Frontend):
- ESLint + Prettier configuration
- Strict TypeScript mode enabled
- Explicit return types for exported functions
- React functional components with TypeScript props

### 5.2 Security Practices

**SQL Injection Prevention**:
```python
# NEVER: Direct string interpolation
query = f"SELECT * FROM users WHERE id = {user_id}"  # FORBIDDEN

# ALWAYS: Parameterized queries
query = "SELECT * FROM users WHERE id = :user_id"
result = await db.execute(query, {"user_id": user_id})
```

**Input Validation**:
```python
from pydantic import BaseModel, validator

class EpisodeUpload(BaseModel):
    title: str
    audio_url: str
    duration: int
    
    @validator("title")
    def validate_title(cls, v):
        if len(v) > 200:
            raise ValueError("Title must be < 200 characters")
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
    
    @validator("duration")
    def validate_duration(cls, v):
        if v < 60 or v > 14400:  # 1 min to 4 hours
            raise ValueError("Duration must be 1-240 minutes")
        return v
```

### 5.3 Naming Conventions

**Variables & Functions**:
- `snake_case` for Python
- `camelCase` for TypeScript
- Descriptive names (no single letters except iterators)
- Boolean variables prefixed with `is_`, `has_`, `should_`

**Classes**:
- `PascalCase` for both Python and TypeScript
- Noun-based names (e.g., `ContentGenerator`, `TranscriptAnalyzer`)

**Files**:
- `snake_case.py` for Python modules
- `PascalCase.tsx` for React components
- Group related code in subdirectories

---

## 6. Self-Debugging & Monitoring

### 6.1 Logging Standards

**Log Levels**:
```python
# DEBUG: Detailed diagnostic info (dev only)
logger.debug(f"Processing segment {segment_id} of {total_segments}")

# INFO: General informational messages
logger.info(f"Started content generation for episode {episode_id}")

# WARNING: Unexpected but handled situations
logger.warning(f"Transcript quality low (score: {score}), results may vary")

# ERROR: Errors that affect single operation
logger.error(f"Failed to generate blog post: {error}", exc_info=True)

# CRITICAL: System-wide failures requiring immediate attention
logger.critical(f"Database connection lost, cannot process jobs")
```

**Structured Logging**:
```python
logger.info(
    "Content generation completed",
    extra={
        "episode_id": episode.id,
        "user_id": user.id,
        "duration_seconds": 87,
        "output_formats": ["blog", "social", "newsletter"],
        "llm_calls": 12,
        "total_cost": 0.43
    }
)
```

### 6.2 Performance Monitoring

**Metric Collection**:
- Track execution time for each agent
- Count LLM API calls and tokens used
- Monitor memory usage per job
- Record user satisfaction ratings

**Alerting Thresholds**:
```python
ALERT_THRESHOLDS = {
    "job_duration_seconds": 600,  # Alert if > 10 min
    "error_rate_percent": 5,       # Alert if > 5% failures
    "api_latency_ms": 5000,        # Alert if > 5s response
    "queue_depth": 100,            # Alert if backlog > 100 jobs
}
```

### 6.3 Self-Diagnosis

**Health Check Protocol**:
```python
async def agent_health_check() -> HealthStatus:
    """
    Periodic self-diagnostic (every 60 seconds)
    """
    checks = {
        "llm_api": await check_llm_connectivity(),
        "database": await check_db_connection(),
        "redis": await check_redis_connection(),
        "s3": await check_s3_access(),
        "memory": check_memory_usage(),
    }
    
    if any(not check.healthy for check in checks.values()):
        await notify_ops_team(checks)
    
    return HealthStatus(
        healthy=all(c.healthy for c in checks.values()),
        checks=checks
    )
```

---

## 7. Interaction Rules with Users

### 7.1 Communication Tone

**Principles**:
- Professional but friendly (avoid corporate jargon)
- Concise and actionable (no unnecessary verbosity)
- Empathetic to user frustrations
- Transparent about limitations

**Good Examples**:
```
✓ "Your content is ready! We found 8 key topics to work with."
✓ "Processing is taking longer than usual. We're working on it."
✓ "We couldn't generate the newsletter because the transcript was too short. Try episodes over 10 minutes."

✗ "Content generation subroutine has completed successfully."
✗ "An error occurred. Please try again later."
✗ "Your input parameters were invalid."
```

### 7.2 Progress Updates

**Update Frequency**:
- Every 15 seconds during active processing
- Immediate notification on completion or error
- Include estimated time remaining when available

**Progress Message Template**:
```json
{
  "status": "processing",
  "stage": "generating_blog_post",
  "progress_percent": 65,
  "message": "Writing blog post sections...",
  "estimated_seconds_remaining": 45
}
```

### 7.3 Error Communication

**User-Facing Error Messages**:
```python
ERROR_MESSAGES = {
    "transcription_failed": {
        "title": "We couldn't transcribe your audio",
        "message": "The audio file may be corrupted or in an unsupported format.",
        "action": "Try uploading a different file or contact support.",
        "code": "TRANS_001"
    },
    "content_too_short": {
        "title": "Episode too short for quality content",
        "message": "We need at least 10 minutes of audio to generate meaningful content.",
        "action": "Upload a longer episode or adjust your content settings.",
        "code": "CONTENT_002"
    }
}
```

**Never expose**:
- Stack traces or technical errors
- API keys or internal URLs
- Database queries or schema details

---

## 8. Quality Assurance Standards

### 8.1 Content Validation Rules

**Factual Accuracy**:
- Every claim must be traceable to transcript
- No external facts or statistics without user permission
- Flag uncertain information with confidence scores

**Brand Voice Compliance**:
- Compare output to user's sample writings
- Compute similarity score (target: 85%+)
- Flag deviations for user review

**SEO Optimization** (Blog Posts):
- Title: 50-60 characters
- Meta description: 150-160 characters
- H2 headers every 300-400 words
- Target keyword density: 1-2%
- Readability: Flesch score 60+

### 8.2 Output Validation Checklist

Before returning content to user:

- [ ] All required fields present (title, content, metadata)
- [ ] No placeholder text or TODO markers
- [ ] Proper formatting (markdown, HTML as specified)
- [ ] Links are valid and properly formatted
- [ ] Images referenced are accessible
- [ ] Character counts within platform limits
- [ ] No profanity (unless user's brand allows)
- [ ] No copyright violations
- [ ] Confidence score > 80%

### 8.3 Rejection Criteria

Outputs must be rejected and regenerated if:
- Contains factual errors (cross-check with transcript)
- Brand voice match < 75%
- Readability score < 50 (too complex)
- Contains prohibited content
- Missing critical components (CTA, headers, etc.)
- Under/over length target by > 20%

---

## 9. Continuous Improvement

### 9.1 Learning from Feedback

**User Rating System**:
- Collect 1-5 star ratings on all outputs
- Request specific feedback on rejected content
- Track which content formats get highest ratings

**Feedback Loop**:
```python
async def process_user_feedback(
    content_id: str,
    rating: int,
    feedback: Optional[str]
):
    """
    Store and learn from user feedback
    """
    await store_feedback(content_id, rating, feedback)
    
    # If rating < 3, analyze for patterns
    if rating < 3:
        await analyze_low_rating(content_id, feedback)
        await adjust_generation_params(content_id)
```

### 9.2 A/B Testing

**Test Variations**:
- Different prompt formulations
- Alternative LLM models
- Various output structures

**Metrics to Track**:
- User satisfaction ratings
- Edit time required
- Publish rate (% of content actually used)

### 9.3 Agent Performance Reviews

**Monthly Analysis**:
- Success rate per agent
- Average processing time
- Cost per successful output
- User satisfaction by agent

**Optimization Triggers**:
- If success rate < 95% → Review prompts
- If cost > target → Optimize model selection
- If satisfaction < 4.0 → Revise generation logic

---

## 10. Emergency Protocols

### 10.1 Circuit Breaker Pattern

**Automatic Shutdown Conditions**:
```python
CIRCUIT_BREAKER_THRESHOLDS = {
    "error_rate": 0.20,        # Stop if > 20% failure rate
    "cost_spike": 5.0,         # Stop if cost > 5x normal
    "api_errors": 50,          # Stop if > 50 API errors/hour
    "memory_usage": 0.90,      # Stop if > 90% memory
}
```

**Recovery Process**:
1. Stop accepting new jobs
2. Complete in-progress jobs if safe
3. Notify operations team
4. Log all context for debugging
5. Wait for manual approval to resume

### 10.2 Data Corruption Response

If data integrity issue detected:
1. Immediately stop all write operations
2. Isolate affected records
3. Notify users of impacted content
4. Restore from last known good backup
5. Conduct root cause analysis

### 10.3 Security Incident Response

If unauthorized access detected:
1. Revoke all active sessions
2. Rotate API keys and secrets
3. Lock affected user accounts
4. Audit all recent activity
5. Notify affected users within 24 hours

---

## Appendix: Rule Compliance Checklist

Before deploying any agent or code change, verify:

- [ ] Agent role clearly defined within scope
- [ ] Chain-of-thought reasoning implemented
- [ ] Error handling with graceful degradation
- [ ] Data access follows least privilege
- [ ] Content safety checks in place
- [ ] Rate limiting enforced
- [ ] Input validation with Pydantic
- [ ] Logging follows structured format
- [ ] User-facing errors are actionable
- [ ] Code follows style guide
- [ ] Security practices implemented
- [ ] Performance monitored
- [ ] Unit tests cover critical paths

---

**Document Version**: 1.2  
**Last Updated**: November 2025  
**Review Cycle**: Quarterly  
**Owned By**: AI Engineering Team