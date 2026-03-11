# R U Serious? - API Documentation

Complete API reference for the R U Serious? backend system.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### POST /auth/login

Login and receive JWT token.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": "USR002",
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "display_name": "John Doe",
    "xp_points": 2450,
    "level": 7
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials

---

### GET /auth/me

Get current authenticated user information.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
{
  "user_id": "USR002",
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user",
  "display_name": "John Doe",
  "avatar_id": "AVT001",
  "language_preference": "en",
  "voice_preference": "male",
  "full_vocal_mode": false,
  "xp_points": 2450,
  "level": 7,
  "streak_days": 12,
  "created_at": "2024-01-05T00:00:00",
  "last_login": "2024-01-15T09:00:00"
}
```

---

## User Endpoints

### GET /users/profile

Get current user's profile.

**Headers:** Requires Authentication

**Response:** `200 OK` - Same as `/auth/me`

---

### PUT /users/profile

Update user profile.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "display_name": "John Smith",
  "email": "john.smith@example.com",
  "avatar_id": "AVT002"
}
```

**Response:** `200 OK` - Updated user object

---

### GET /users/history

Get learning history.

**Headers:** Requires Authentication

**Query Parameters:**
- `limit` (optional, default: 50) - Max records to return
- `offset` (optional, default: 0) - Records to skip

**Response:** `200 OK`
```json
[
  {
    "history_id": "HIS001",
    "user_id": "USR002",
    "session_id": "SES001",
    "content_type": "image",
    "content_id": "IMG001",
    "content_path": "generated_images/ses001_img001.png",
    "topic": "Photosynthesis",
    "viewed_at": "2024-01-15T09:01:00"
  }
]
```

---

### PUT /users/settings

Update user settings.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "language_preference": "hi",
  "voice_preference": "female",
  "full_vocal_mode": true,
  "notifications_enabled": true,
  "sound_enabled": true,
  "auto_play_videos": true,
  "theme": "dark"
}
```

**Response:** `200 OK` - Updated settings object

---

## Learning Session Endpoints

### POST /learning/start

Start a new learning session.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "topic": "Photosynthesis",
  "difficulty_level": 5,
  "duration_minutes": 15,
  "visual_style": "cartoon",
  "play_mode": "solo",
  "team_id": null,
  "tournament_id": null,
  "avatar_id": "AVT001",
  "character_ids": ["CHR001", "CHR002"]
}
```

**Response:** `201 Created`
```json
{
  "session_id": "SES001",
  "user_id": "USR002",
  "topic": "Photosynthesis",
  "difficulty_level": 5,
  "duration_minutes": 15,
  "visual_style": "cartoon",
  "play_mode": "solo",
  "status": "in_progress",
  "current_cycle": 0,
  "total_cycles": 3,
  "score": 0,
  "started_at": "2024-01-15T09:00:00"
}
```

---

### GET /learning/session/{session_id}/content

Get generated learning content for a session.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
{
  "session_id": "SES001",
  "topic": "Photosynthesis",
  "story_segments": [
    {
      "segment_number": 1,
      "narrative": "In a sunny garden, plants use sunlight to make their own food...",
      "facts": [
        "Photosynthesis occurs in chloroplasts",
        "Plants absorb carbon dioxide from air"
      ],
      "image_prompt": "Cartoon illustration of plant cells with chloroplasts...",
      "image_url": "/media/generated_images/ses_SES001_img_1.png",
      "audio_url": null
    }
  ],
  "topic_summary": "Photosynthesis is the process plants use to convert light energy into chemical energy.",
  "total_cycles": 3
}
```

---

### POST /learning/session/{session_id}/progress

Update session progress.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "current_cycle": 2,
  "score": 85,
  "time_spent_seconds": 450
}
```

**Response:** `200 OK`
```json
{
  "message": "Progress updated successfully",
  "session": { /* updated session object */ }
}
```

---

### POST /learning/session/{session_id}/end

End a learning session.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "final_score": 450,
  "total_time_seconds": 1080,
  "completed": true
}
```

**Response:** `200 OK`
```json
{
  "session_id": "SES001",
  "topic": "Photosynthesis",
  "difficulty_level": 5,
  "duration_minutes": 15,
  "score": 450,
  "total_questions": 6,
  "correct_answers": 5,
  "accuracy_rate": 83.33,
  "xp_earned": 2250,
  "time_spent_seconds": 1080,
  "completed_at": "2024-01-15T09:18:00"
}
```

---

## Quiz Endpoints

### GET /quiz/session/{session_id}/mcq

Get MCQ questions for a session.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
[
  {
    "question_id": "Q001",
    "question_text": "What is the primary pigment involved in photosynthesis?",
    "options": {
      "A": "Melanin",
      "B": "Chlorophyll",
      "C": "Hemoglobin",
      "D": "Carotene"
    },
    "image_url": null
  }
]
```

---

### POST /quiz/session/{session_id}/mcq/answer

Submit MCQ answer.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "question_id": "Q001",
  "selected_answer": "B"
}
```

**Response:** `200 OK`
```json
{
  "question_id": "Q001",
  "selected_answer": "B",
  "correct_answer": "B",
  "is_correct": true,
  "explanation": "Chlorophyll is the green pigment that captures light energy for photosynthesis.",
  "points_earned": 10,
  "time_taken_seconds": 30
}
```

---

### GET /quiz/session/{session_id}/descriptive

Get descriptive questions for a session.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
[
  {
    "question_id": "DQ001",
    "question_text": "Explain how photosynthesis helps maintain Earth's atmosphere.",
    "max_score": 10
  }
]
```

---

### POST /quiz/session/{session_id}/descriptive/answer

Submit descriptive answer for AI evaluation.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "question_id": "DQ001",
  "answer_text": "Photosynthesis helps by absorbing CO2 and releasing oxygen into the atmosphere..."
}
```

**Response:** `200 OK`
```json
{
  "question_id": "DQ001",
  "user_answer": "Photosynthesis helps by absorbing CO2...",
  "score": 8,
  "max_score": 10,
  "feedback": {
    "correct_points": [
      "Correctly mentioned CO2 absorption",
      "Correctly mentioned oxygen release"
    ],
    "improvements": [
      "Could mention the role of glucose production"
    ],
    "explanation": "Good answer covering main points. Consider adding more detail about glucose."
  },
  "points_earned": 8,
  "time_taken_seconds": 60
}
```

---

## Avatar Endpoints

### GET /avatar/list

Get list of user's avatars.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
[
  {
    "avatar_id": "AVT001",
    "user_id": "USR002",
    "name": "Explorer Raj",
    "image_path": "avatars/avt001.png",
    "image_url": "/media/avatars/avt001.png",
    "creation_method": "upload",
    "style": "cartoon",
    "created_at": "2024-01-05T00:00:00"
  }
]
```

---

### POST /avatar/upload

Create avatar from uploaded image.

**Headers:** Requires Authentication

**Request:** `multipart/form-data`
- `file`: Image file
- `name`: Avatar name
- `style`: "cartoon" or "realistic"

**Response:** `201 Created` - Avatar object

---

### POST /avatar/draw

Create avatar from drawing canvas data.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "drawing_data": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "name": "My Drawing",
  "style": "cartoon"
}
```

**Response:** `201 Created` - Avatar object

---

### GET /avatar/gallery

Get list of default/pre-made avatars.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
[
  {
    "avatar_id": "DEFAULT_001",
    "name": "Explorer",
    "image_url": "/media/default-avatars/explorer.png",
    "style": "cartoon"
  }
]
```

---

## Character Endpoints

### GET /characters/list

Get list of user's characters.

**Headers:** Requires Authentication

**Response:** `200 OK` - Array of character objects

---

### POST /characters/create

Create a new character.

**Headers:** Requires Authentication

**Request:** `multipart/form-data`
- `file`: Image file
- `name`: Character name
- `description`: Character description
- `creation_method`: "upload", "draw", or "gallery"

**Response:** `201 Created` - Character object

---

### DELETE /characters/{character_id}

Delete a character.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
{
  "message": "Character deleted successfully",
  "character_id": "CHR001"
}
```

---

## Voice Endpoints

### POST /voice/tts

Convert text to speech.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "text": "Hello, welcome to R U Serious?",
  "language": "en",
  "voice_type": "female",
  "speed": 1.0
}
```

**Response:** `200 OK` - Audio file (MP3)

---

### POST /voice/stt

Convert speech to text.

**Headers:** Requires Authentication

**Request:** `multipart/form-data`
- `audio`: Audio file (WAV/MP3)
- `language`: Language code (e.g., "en", "hi")

**Response:** `200 OK`
```json
{
  "transcribed_text": "Hello world",
  "language": "en"
}
```

---

## Video Endpoints

### GET /video/session/{session_id}/cycle/{cycle_number}

Get or generate video for a cycle.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
{
  "session_id": "SES001",
  "cycle_number": 1,
  "status": "ready",
  "video_url": "/media/generated_videos/ses_SES001_cycle_1.mp4",
  "progress_percent": 100
}
```

**Possible status values:** `generating`, `ready`, `failed`

---

### GET /video/session/{session_id}/cycle/{cycle_number}/status

Check video generation status.

**Headers:** Requires Authentication

**Response:** `200 OK` - Same as above endpoint

---

## Tournament Endpoints

### GET /tournaments/list

Get list of tournaments.

**Headers:** Requires Authentication

**Query Parameters:**
- `status_filter` (optional) - Filter by: "upcoming", "active", "completed"

**Response:** `200 OK` - Array of tournament objects

---

### POST /tournaments/{tournament_id}/join

Join a tournament.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "team_id": "TM001"
}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully joined tournament",
  "tournament_id": "TRN001",
  "team_id": "TM001"
}
```

---

### GET /tournaments/leaderboard

Get leaderboard.

**Headers:** Requires Authentication

**Query Parameters:**
- `scope` - "global" or "tournament"
- `tournament_id` (required if scope=tournament)
- `limit` (optional, default: 100)

**Response:** `200 OK`
```json
[
  {
    "rank": 1,
    "user_id": "USR005",
    "display_name": "Sarah Wilson",
    "score": 3200,
    "avatar_url": "/media/avatars/AVT005.png"
  }
]
```

---

## Team Endpoints

### GET /teams/list

Get list of all teams.

**Headers:** Requires Authentication

**Response:** `200 OK` - Array of team objects with members

---

### POST /teams/create

Create a new team.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "name": "Science Stars"
}
```

**Response:** `201 Created` - Team object

---

### POST /teams/{team_id}/join

Join an existing team.

**Headers:** Requires Authentication

**Response:** `200 OK`
```json
{
  "message": "Successfully joined team",
  "team_id": "TM001",
  "team_name": "Science Stars"
}
```

---

### GET /teams/{team_id}

Get team details.

**Headers:** Requires Authentication

**Response:** `200 OK` - Team object with full member list

---

## Chat Endpoint

### POST /chat/message

Send a chat message to AI.

**Headers:** Requires Authentication

**Request Body:**
```json
{
  "message": "What is photosynthesis?",
  "context": "We are learning about plants",
  "language": "en"
}
```

**Response:** `200 OK`
```json
{
  "response": "Photosynthesis is the process by which plants...",
  "language": "en"
}
```

---

## Admin Endpoints

All admin endpoints require the user to have `role: "admin"`.

### POST /admin/tournaments/create

Create a new tournament.

**Headers:** Requires Admin Authentication

**Request Body:**
```json
{
  "name": "Science Masters 2024",
  "topic": "General Science",
  "difficulty_level": 6,
  "start_datetime": "2024-01-20T10:00:00",
  "end_datetime": "2024-01-20T12:00:00",
  "duration_minutes": 120,
  "max_participants": 100,
  "team_size_min": 1,
  "team_size_max": 5,
  "entry_type": "free",
  "status": "upcoming",
  "prize_1st": "Gold Badge + 500 XP",
  "prize_2nd": "Silver Badge + 300 XP",
  "prize_3rd": "Bronze Badge + 100 XP"
}
```

**Response:** `201 Created` - Tournament object

---

### POST /admin/questions/upload

Upload questions from CSV file.

**Headers:** Requires Admin Authentication

**Request:** `multipart/form-data`
- `file`: CSV file with questions
- `question_type`: "mcq" or "descriptive"

**CSV Format for MCQ:**
```
topic,difficulty_level,question_text,option_a,option_b,option_c,option_d,correct_answer,explanation
```

**CSV Format for Descriptive:**
```
topic,difficulty_level,question_text,model_answer,keywords,max_score
```

**Response:** `201 Created`
```json
{
  "message": "Successfully uploaded 10 questions",
  "uploaded_count": 10,
  "total_rows": 10,
  "errors": null
}
```

---

### GET /admin/users

Get all users.

**Headers:** Requires Admin Authentication

**Query Parameters:**
- `limit` (optional, default: 100)
- `offset` (optional, default: 0)

**Response:** `200 OK` - Array of user objects

---

## Health Check

### GET /health

Check system health and provider status.

**No Authentication Required**

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "providers": {
    "ai": {
      "provider": "GeminiProvider",
      "status": "healthy"
    },
    "image": {
      "provider": "FiboProvider",
      "status": "healthy"
    },
    "tts": {
      "provider": "GCPTTSProvider",
      "status": "healthy"
    },
    "stt": {
      "provider": "GCPSTTProvider",
      "status": "healthy"
    }
  },
  "version": "1.0.0-prototype"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

### Common HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Currently not implemented in prototype. In production, implement rate limiting per endpoint.

## Pagination

Endpoints that return lists support pagination via `limit` and `offset` query parameters.

---

For interactive API testing, visit: http://localhost:8000/docs
