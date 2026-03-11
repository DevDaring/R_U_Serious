# R U Serious? - Backend

Production-ready FastAPI backend for the R U Serious? adaptive learning system.

## Features

- **RESTful API** with FastAPI
- **JWT Authentication** with secure password hashing
- **Modular Provider System** - Switch AI/Image/Voice providers via environment variables
- **CSV-based Database** for prototype data storage
- **Async/Await** support for optimal performance
- **Comprehensive Error Handling**
- **Auto-generated API Documentation** (Swagger/OpenAPI)
- **CORS Support** for frontend integration
- **Static File Serving** for generated media

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/         # API route handlers
│   │   │   ├── auth.py     # Authentication endpoints
│   │   │   ├── users.py    # User profile & settings
│   │   │   ├── learning.py # Learning sessions
│   │   │   ├── quiz.py     # MCQ & descriptive questions
│   │   │   ├── avatar.py   # Avatar management
│   │   │   ├── characters.py # Character management
│   │   │   ├── voice.py    # TTS & STT
│   │   │   ├── video.py    # Video generation
│   │   │   ├── tournaments.py # Tournament system
│   │   │   ├── teams.py    # Team management
│   │   │   ├── chat.py     # AI chat
│   │   │   └── admin.py    # Admin endpoints
│   │   └── dependencies.py # Auth & shared dependencies
│   ├── services/           # Business logic services
│   ├── database/           # CSV handlers
│   ├── models/             # Pydantic models
│   ├── utils/              # Helper functions
│   ├── config.py           # Configuration settings
│   └── main.py             # FastAPI application
├── data/
│   ├── csv/                # CSV database files
│   └── media/              # Generated media files
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# Minimum required:
# - GEMINI_API_KEY
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 3. Run the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `GET /api/users/history` - Learning history
- `PUT /api/users/settings` - Update settings

### Learning Sessions
- `POST /api/learning/start` - Start new session
- `GET /api/learning/session/{id}/content` - Get learning content
- `POST /api/learning/session/{id}/progress` - Update progress
- `POST /api/learning/session/{id}/end` - End session

### Quiz
- `GET /api/quiz/session/{id}/mcq` - Get MCQ questions
- `POST /api/quiz/session/{id}/mcq/answer` - Submit MCQ answer
- `GET /api/quiz/session/{id}/descriptive` - Get descriptive questions
- `POST /api/quiz/session/{id}/descriptive/answer` - Submit descriptive answer

### Avatar & Characters
- `GET /api/avatar/list` - List user avatars
- `POST /api/avatar/upload` - Create avatar from upload
- `POST /api/avatar/draw` - Create avatar from drawing
- `GET /api/avatar/gallery` - Get default avatars
- `GET /api/characters/list` - List user characters
- `POST /api/characters/create` - Create character
- `DELETE /api/characters/{id}` - Delete character

### Voice
- `POST /api/voice/tts` - Text-to-Speech
- `POST /api/voice/stt` - Speech-to-Text

### Video
- `GET /api/video/session/{id}/cycle/{n}` - Get/generate video
- `GET /api/video/session/{id}/cycle/{n}/status` - Check video status

### Tournaments & Teams
- `GET /api/tournaments/list` - List tournaments
- `POST /api/tournaments/{id}/join` - Join tournament
- `GET /api/tournaments/leaderboard` - Get leaderboard
- `GET /api/teams/list` - List teams
- `POST /api/teams/create` - Create team
- `POST /api/teams/{id}/join` - Join team
- `GET /api/teams/{id}` - Get team details

### Chat
- `POST /api/chat/message` - Send chat message

### Admin (Requires admin role)
- `POST /api/admin/tournaments/create` - Create tournament
- `POST /api/admin/questions/upload` - Upload questions CSV
- `GET /api/admin/users` - List all users

## Authentication

All endpoints (except `/api/auth/login`) require JWT authentication:

```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/users/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `password123`

**Test User Account:**
- Username: `john_doe`
- Password: `password123`

> ⚠️ **Change these passwords in production!**

## Provider Configuration

Switch AI/Image/Voice providers by changing environment variables:

### AI Providers (Content Generation)
```env
AI_PROVIDER=gemini    # Options: gemini, openai, anthropic
GEMINI_API_KEY=your_key
```

### Image Providers (Image Generation)
```env
IMAGE_PROVIDER=fibo   # Options: fibo, stability
FIBO_API_KEY=your_key
```

### Voice Providers (TTS/STT)
```env
VOICE_TTS_PROVIDER=gcp  # Options: gcp, azure
VOICE_STT_PROVIDER=gcp  # Options: gcp, azure
GCP_TTS_API_KEY=your_key
GCP_STT_API_KEY=your_key
```

**No code changes required!** The `ProviderFactory` handles everything automatically.

## Error Handling

All endpoints return standardized error responses:

```json
{
  "detail": "Error message here"
}
```

HTTP Status Codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Type Checking
```bash
mypy app/
```

## CSV Database Schema

### users.csv
- user_id, username, email, password_hash, role, display_name
- avatar_id, language_preference, voice_preference, full_vocal_mode
- xp_points, level, streak_days, created_at, last_login

### sessions.csv
- session_id, user_id, topic, difficulty_level, duration_minutes
- visual_style, play_mode, team_id, tournament_id
- status, current_cycle, total_cycles, score
- started_at, completed_at

### questions_mcq.csv
- question_id, topic, difficulty_level, question_text
- option_a, option_b, option_c, option_d
- correct_answer, explanation, created_by, is_ai_generated, created_at

### questions_descriptive.csv
- question_id, topic, difficulty_level, question_text
- model_answer, keywords, max_score
- created_by, is_ai_generated, created_at

See `genlearn-ai-prompt.md` for complete schema documentation.

## Production Deployment

### Environment Variables
- Set `APP_ENV=production`
- Set `DEBUG=false`
- Use strong `SECRET_KEY`
- Configure proper `BACKEND_HOST` and `BACKEND_PORT`

### Security Checklist
- [ ] Change default passwords
- [ ] Use environment-based secrets management
- [ ] Enable HTTPS/TLS
- [ ] Configure rate limiting
- [ ] Set up proper CORS origins
- [ ] Enable request logging
- [ ] Set up monitoring and alerts

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

### Import Errors
```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Provider Connection Issues
```bash
# Check provider health
curl http://localhost:8000/health

# Verify API keys in .env file
cat .env | grep API_KEY
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write docstrings for all public functions
4. Add proper error handling
5. Update API documentation
6. Test all endpoints before committing

## License

This project is part of the R U Serious? prototype system.

## Support

For issues and questions, refer to the main project documentation in `genlearn-ai-prompt.md`.
