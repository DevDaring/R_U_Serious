# GenLearn AI - Complete Prototype Development Prompt

## PROJECT OVERVIEW

Build a **GenLearn AI** prototype - a Generative AI-enabled adaptive learning system. This is a full-stack application with React+Vite+TypeScript frontend and Python FastAPI backend. The prototype uses CSV files for data storage and local folders for multimedia assets.

---

## TECHNOLOGY STACK

### Frontend
- **Framework**: React 18 + Vite + TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand or React Context
- **HTTP Client**: Axios
- **Audio**: Web Audio API for recording/playback
- **Canvas**: Fabric.js or React-Konva for drawing

### Backend
- **Framework**: Python 3.11+ with FastAPI
- **Database**: CSV files (pandas for manipulation)
- **File Storage**: Local folders
- **API Integration**: httpx for async HTTP calls
- **Audio Processing**: pydub (optional)
- **Environment**: python-dotenv

---

## PROJECT STRUCTURE

Create the following directory structure:

```
genlearn-ai/
├── frontend/
│   ├── public/
│   │   └── assets/
│   │       ├── icons/
│   │       └── default-avatars/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── TopNavbar.tsx
│   │   │   │   ├── LeftMenu.tsx
│   │   │   │   ├── RightPanel.tsx
│   │   │   │   ├── MainContent.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── learning/
│   │   │   │   ├── CourseSetup.tsx
│   │   │   │   ├── ImageCard.tsx
│   │   │   │   ├── ImageCarousel.tsx
│   │   │   │   ├── MCQQuiz.tsx
│   │   │   │   ├── DescriptiveQuestion.tsx
│   │   │   │   ├── VideoPlayer.tsx
│   │   │   │   └── LearningSession.tsx
│   │   │   ├── avatar/
│   │   │   │   ├── AvatarCreator.tsx
│   │   │   │   ├── DrawingCanvas.tsx
│   │   │   │   ├── ImageUploader.tsx
│   │   │   │   └── AvatarGallery.tsx
│   │   │   ├── characters/
│   │   │   │   ├── CharacterManager.tsx
│   │   │   │   └── CharacterCard.tsx
│   │   │   ├── gamification/
│   │   │   │   ├── Scoreboard.tsx
│   │   │   │   ├── TeamSelector.tsx
│   │   │   │   ├── TournamentList.tsx
│   │   │   │   └── TournamentCard.tsx
│   │   │   ├── admin/
│   │   │   │   ├── AdminDashboard.tsx
│   │   │   │   ├── TournamentCreator.tsx
│   │   │   │   ├── TeamManager.tsx
│   │   │   │   ├── QuestionUploader.tsx
│   │   │   │   └── UserManager.tsx
│   │   │   ├── voice/
│   │   │   │   ├── VoiceInput.tsx
│   │   │   │   ├── VoiceOutput.tsx
│   │   │   │   ├── FullVocalMode.tsx
│   │   │   │   └── LanguageSelector.tsx
│   │   │   ├── chat/
│   │   │   │   ├── ChatWindow.tsx
│   │   │   │   └── ChatMessage.tsx
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── Dropdown.tsx
│   │   │       ├── Slider.tsx
│   │   │       ├── LoadingSpinner.tsx
│   │   │       ├── ProgressBar.tsx
│   │   │       └── Toast.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── LearningPage.tsx
│   │   │   ├── AvatarPage.tsx
│   │   │   ├── CharactersPage.tsx
│   │   │   ├── TournamentsPage.tsx
│   │   │   ├── LeaderboardPage.tsx
│   │   │   ├── ProfilePage.tsx
│   │   │   ├── SettingsPage.tsx
│   │   │   ├── HistoryPage.tsx
│   │   │   └── admin/
│   │   │       ├── AdminHomePage.tsx
│   │   │       ├── ManageTournamentsPage.tsx
│   │   │       ├── ManageTeamsPage.tsx
│   │   │       ├── ManageQuestionsPage.tsx
│   │   │       └── ManageUsersPage.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useVoice.ts
│   │   │   ├── useLearningSession.ts
│   │   │   ├── useFullVocalMode.ts
│   │   │   └── useApi.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── store/
│   │   │   ├── authStore.ts
│   │   │   ├── learningStore.ts
│   │   │   ├── settingsStore.ts
│   │   │   └── voiceStore.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   ├── helpers.ts
│   │   │   └── constants.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── learning.py
│   │   │   │   ├── avatar.py
│   │   │   │   ├── characters.py
│   │   │   │   ├── quiz.py
│   │   │   │   ├── voice.py
│   │   │   │   ├── video.py
│   │   │   │   ├── tournaments.py
│   │   │   │   ├── teams.py
│   │   │   │   ├── admin.py
│   │   │   │   └── chat.py
│   │   │   └── dependencies.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py          # Abstract base class
│   │   │   │   ├── gemini.py        # Google Gemini 3
│   │   │   │   ├── openai.py        # OpenAI (fallback)
│   │   │   │   └── anthropic.py     # Anthropic (fallback)
│   │   │   ├── image_providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py          # Abstract base class
│   │   │   │   ├── fibo.py          # FIBO API
│   │   │   │   └── stability.py     # Stability AI (fallback)
│   │   │   ├── voice_providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py          # Abstract base class
│   │   │   │   ├── gcp_tts.py       # GCP Text-to-Speech
│   │   │   │   ├── gcp_stt.py       # GCP Speech-to-Text
│   │   │   │   └── azure_voice.py   # Azure (fallback)
│   │   │   ├── provider_factory.py  # Factory to get providers
│   │   │   ├── content_generator.py
│   │   │   ├── question_generator.py
│   │   │   ├── answer_evaluator.py
│   │   │   ├── video_generator.py
│   │   │   ├── avatar_service.py
│   │   │   └── scoring_service.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── csv_handler.py       # CSV CRUD operations
│   │   │   └── file_handler.py      # File operations
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── quiz.py
│   │   │   ├── tournament.py
│   │   │   ├── team.py
│   │   │   └── avatar.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── helpers.py
│   │       └── validators.py
│   ├── data/
│   │   ├── csv/
│   │   │   ├── users.csv
│   │   │   ├── sessions.csv
│   │   │   ├── scores.csv
│   │   │   ├── questions_mcq.csv
│   │   │   ├── questions_descriptive.csv
│   │   │   ├── tournaments.csv
│   │   │   ├── teams.csv
│   │   │   ├── team_members.csv
│   │   │   ├── avatars.csv
│   │   │   ├── characters.csv
│   │   │   └── learning_history.csv
│   │   └── media/
│   │       ├── avatars/
│   │       ├── characters/
│   │       ├── generated_images/
│   │       ├── generated_videos/
│   │       ├── audio/
│   │       └── uploads/
│   ├── requirements.txt
│   └── .env
│
├── docs/
│   └── env.md
│
├── .gitignore
└── README.md
```

---

## ENVIRONMENT CONFIGURATION

### Create `docs/env.md` with this template:

```markdown
# Environment Variables Template

Copy this content to `backend/.env` and fill in your API keys.

## Required API Keys

### Google Cloud Platform (Primary)
```env
# Gemini 3 API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3-pro-preview

# GCP Speech-to-Text
GCP_PROJECT_ID=your_gcp_project_id
GCP_STT_API_KEY=your_gcp_stt_api_key
GCP_STT_ENDPOINT=https://speech.googleapis.com/v1

# GCP Text-to-Speech
GCP_TTS_API_KEY=your_gcp_tts_api_key
GCP_TTS_ENDPOINT=https://texttospeech.googleapis.com/v1
```

### Image Generation
```env
# FIBO API (Primary)
FIBO_API_KEY=your_fibo_api_key_here
FIBO_API_ENDPOINT=https://api.fibo.ai/v1

# Stability AI (Fallback)
STABILITY_API_KEY=your_stability_api_key_here
```

### Fallback AI Providers (Optional)
```env
# OpenAI (Fallback for Gemini)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Fallback for Gemini)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Application Configuration
```env
# App Settings
APP_NAME=GenLearn AI
APP_ENV=development
DEBUG=true
SECRET_KEY=your_random_secret_key_for_jwt

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# Provider Selection (change these to switch providers)
AI_PROVIDER=gemini          # Options: gemini, openai, anthropic
IMAGE_PROVIDER=fibo         # Options: fibo, stability
VOICE_TTS_PROVIDER=gcp      # Options: gcp, azure
VOICE_STT_PROVIDER=gcp      # Options: gcp, azure

# File Paths
DATA_DIR=./data
CSV_DIR=./data/csv
MEDIA_DIR=./data/media
```

## Notes
- Never commit the .env file to version control
- Keep API keys secure and rotate them periodically
- For production, use proper secrets management
```

---

## CSV DATABASE SCHEMAS

### Create these CSV files with headers and sample data:

### `data/csv/users.csv`
```csv
user_id,username,email,password_hash,role,display_name,avatar_id,language_preference,voice_preference,full_vocal_mode,xp_points,level,streak_days,created_at,last_login
USR001,admin,admin@genlearn.ai,$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4NwKXkLQPHHKq0Ky,admin,Administrator,,en,female,false,0,1,0,2024-01-01T00:00:00,2024-01-15T10:30:00
USR002,john_doe,john@example.com,$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4NwKXkLQPHHKq0Ky,user,John Doe,AVT001,en,male,false,2450,7,12,2024-01-05T00:00:00,2024-01-15T09:00:00
USR003,priya_sharma,priya@example.com,$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4NwKXkLQPHHKq0Ky,user,Priya Sharma,AVT002,hi,female,false,1820,5,8,2024-01-08T00:00:00,2024-01-14T18:45:00
USR004,amit_roy,amit@example.com,$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4NwKXkLQPHHKq0Ky,user,Amit Roy,AVT003,bn,male,true,980,3,3,2024-01-10T00:00:00,2024-01-15T11:20:00
USR005,sarah_wilson,sarah@example.com,$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4NwKXkLQPHHKq0Ky,user,Sarah Wilson,,en,female,false,3200,9,25,2024-01-02T00:00:00,2024-01-15T08:15:00
```

**Note**: All sample passwords are hashed version of "password123". In production, use proper password hashing.

### `data/csv/sessions.csv`
```csv
session_id,user_id,topic,difficulty_level,duration_minutes,visual_style,play_mode,team_id,tournament_id,status,current_cycle,total_cycles,score,started_at,completed_at
SES001,USR002,Photosynthesis,5,15,cartoon,solo,,,completed,3,3,450,2024-01-15T09:00:00,2024-01-15T09:18:00
SES002,USR003,Indian History,4,20,realistic,solo,,,in_progress,2,4,280,2024-01-15T18:00:00,
SES003,USR004,Python Basics,3,10,cartoon,team,TM001,,completed,2,2,320,2024-01-14T14:00:00,2024-01-14T14:12:00
```

### `data/csv/scores.csv`
```csv
score_id,user_id,session_id,question_id,question_type,user_answer,is_correct,points_earned,time_taken_seconds,evaluated_at
SCR001,USR002,SES001,Q001,mcq,B,true,10,8,2024-01-15T09:05:00
SCR002,USR002,SES001,Q002,mcq,A,false,2,12,2024-01-15T09:06:00
SCR003,USR002,SES001,DQ001,descriptive,Plants use sunlight to make food through chlorophyll,true,8,45,2024-01-15T09:10:00
```

### `data/csv/questions_mcq.csv`
```csv
question_id,topic,difficulty_level,question_text,option_a,option_b,option_c,option_d,correct_answer,explanation,created_by,is_ai_generated,created_at
Q001,Photosynthesis,5,What is the primary pigment involved in photosynthesis?,Melanin,Chlorophyll,Hemoglobin,Carotene,B,Chlorophyll is the green pigment that captures light energy for photosynthesis.,admin,false,2024-01-01T00:00:00
Q002,Photosynthesis,5,Where does photosynthesis primarily occur in a plant cell?,Nucleus,Mitochondria,Chloroplast,Cell membrane,C,Chloroplasts contain chlorophyll and are the site of photosynthesis.,admin,false,2024-01-01T00:00:00
Q003,Python Basics,3,What keyword is used to define a function in Python?,function,def,func,define,B,The 'def' keyword is used to define functions in Python.,admin,false,2024-01-01T00:00:00
```

### `data/csv/questions_descriptive.csv`
```csv
question_id,topic,difficulty_level,question_text,model_answer,keywords,max_score,created_by,is_ai_generated,created_at
DQ001,Photosynthesis,5,Explain how photosynthesis helps maintain Earth's atmosphere.,"Photosynthesis helps maintain Earth's atmosphere by absorbing carbon dioxide and releasing oxygen. Plants take in CO2 from the air and, using sunlight energy, convert it into glucose while releasing O2 as a byproduct. This process is essential for maintaining the oxygen levels needed by most living organisms and helps regulate atmospheric CO2 levels.","carbon dioxide,oxygen,sunlight,glucose,atmosphere,plants",10,admin,false,2024-01-01T00:00:00
DQ002,Python Basics,3,Explain the difference between a list and a tuple in Python.,"Lists are mutable sequences in Python, meaning their contents can be changed after creation. Tuples are immutable sequences that cannot be modified once created. Lists use square brackets [] while tuples use parentheses (). Tuples are generally faster and use less memory than lists.","mutable,immutable,list,tuple,brackets,parentheses",10,admin,false,2024-01-01T00:00:00
```

### `data/csv/tournaments.csv`
```csv
tournament_id,name,topic,difficulty_level,start_datetime,end_datetime,duration_minutes,max_participants,team_size_min,team_size_max,entry_type,status,prize_1st,prize_2nd,prize_3rd,created_by,created_at
TRN001,Science Masters 2024,General Science,6,2024-01-20T10:00:00,2024-01-20T12:00:00,120,100,1,5,free,upcoming,Gold Badge + 500 XP,Silver Badge + 300 XP,Bronze Badge + 100 XP,USR001,2024-01-10T00:00:00
TRN002,Python Challenge,Python Programming,5,2024-01-18T14:00:00,2024-01-18T15:30:00,90,50,1,3,invite_only,active,500 XP,300 XP,150 XP,USR001,2024-01-08T00:00:00
```

### `data/csv/teams.csv`
```csv
team_id,team_name,created_by,tournament_id,total_score,rank,created_at
TM001,Science Stars,USR002,,4500,1,2024-01-05T00:00:00
TM002,Code Warriors,USR005,TRN002,3200,2,2024-01-10T00:00:00
TM003,Brain Squad,USR003,,2800,3,2024-01-12T00:00:00
```

### `data/csv/team_members.csv`
```csv
membership_id,team_id,user_id,role,joined_at
TM001_USR002,TM001,USR002,leader,2024-01-05T00:00:00
TM001_USR003,TM001,USR003,member,2024-01-06T00:00:00
TM002_USR005,TM002,USR005,leader,2024-01-10T00:00:00
TM002_USR002,TM002,USR002,member,2024-01-11T00:00:00
```

### `data/csv/avatars.csv`
```csv
avatar_id,user_id,name,image_path,creation_method,style,created_at
AVT001,USR002,Explorer Raj,avatars/avt001.png,upload,cartoon,2024-01-05T00:00:00
AVT002,USR003,Curious Priya,avatars/avt002.png,draw,cartoon,2024-01-08T00:00:00
AVT003,USR004,Thinker Amit,avatars/avt003.png,gallery,realistic,2024-01-10T00:00:00
```

### `data/csv/characters.csv`
```csv
character_id,user_id,name,image_path,creation_method,description,created_at
CHR001,USR002,Luna the Fairy,characters/chr001.png,draw,A magical fairy who loves science,2024-01-06T00:00:00
CHR002,USR002,Professor Oak,characters/chr002.png,upload,A wise old owl who teaches,2024-01-07T00:00:00
CHR003,USR003,Ganesha Guide,characters/chr003.png,gallery,A friendly elephant companion,2024-01-09T00:00:00
```

### `data/csv/learning_history.csv`
```csv
history_id,user_id,session_id,content_type,content_id,content_path,topic,viewed_at
HIS001,USR002,SES001,image,IMG001,generated_images/ses001_img001.png,Photosynthesis,2024-01-15T09:01:00
HIS002,USR002,SES001,image,IMG002,generated_images/ses001_img002.png,Photosynthesis,2024-01-15T09:02:00
HIS003,USR002,SES001,video,VID001,generated_videos/ses001_vid001.mp4,Photosynthesis,2024-01-15T09:08:00
```

---

## API PROVIDER ABSTRACTION LAYER

### Create `backend/app/services/provider_factory.py`:

This is the SINGLE PAGE where you change providers. This factory pattern allows switching AI, Image, and Voice providers by simply changing environment variables.

```python
"""
Provider Factory - SINGLE POINT OF CONFIGURATION FOR ALL API PROVIDERS

To switch providers, change the corresponding environment variable:
- AI_PROVIDER: gemini, openai, anthropic
- IMAGE_PROVIDER: fibo, stability
- VOICE_TTS_PROVIDER: gcp, azure
- VOICE_STT_PROVIDER: gcp, azure

No other code changes required!
"""

import os
from typing import Optional
from app.services.ai_providers.base import BaseAIProvider
from app.services.ai_providers.gemini import GeminiProvider
from app.services.ai_providers.openai import OpenAIProvider
from app.services.ai_providers.anthropic import AnthropicProvider
from app.services.image_providers.base import BaseImageProvider
from app.services.image_providers.fibo import FiboProvider
from app.services.image_providers.stability import StabilityProvider
from app.services.voice_providers.base import BaseTTSProvider, BaseSTTProvider
from app.services.voice_providers.gcp_tts import GCPTTSProvider
from app.services.voice_providers.gcp_stt import GCPSTTProvider
from app.services.voice_providers.azure_voice import AzureTTSProvider, AzureSTTProvider


class ProviderFactory:
    """
    Factory class to instantiate the correct provider based on configuration.
    
    USAGE:
        from app.services.provider_factory import ProviderFactory
        
        ai = ProviderFactory.get_ai_provider()
        image = ProviderFactory.get_image_provider()
        tts = ProviderFactory.get_tts_provider()
        stt = ProviderFactory.get_stt_provider()
    """
    
    # ============================================================
    # AI PROVIDERS (for content generation, question creation, etc.)
    # ============================================================
    
    _ai_providers = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
    }
    
    @classmethod
    def get_ai_provider(cls, provider_name: Optional[str] = None) -> BaseAIProvider:
        """
        Get AI provider instance.
        
        Args:
            provider_name: Override provider (optional). 
                          If None, uses AI_PROVIDER env var.
        
        Returns:
            Configured AI provider instance
        """
        name = provider_name or os.getenv("AI_PROVIDER", "gemini")
        provider_class = cls._ai_providers.get(name.lower())
        
        if not provider_class:
            raise ValueError(
                f"Unknown AI provider: {name}. "
                f"Available: {list(cls._ai_providers.keys())}"
            )
        
        return provider_class()
    
    # ============================================================
    # IMAGE PROVIDERS (for image generation)
    # ============================================================
    
    _image_providers = {
        "fibo": FiboProvider,
        "stability": StabilityProvider,
    }
    
    @classmethod
    def get_image_provider(cls, provider_name: Optional[str] = None) -> BaseImageProvider:
        """
        Get Image provider instance.
        
        Args:
            provider_name: Override provider (optional).
                          If None, uses IMAGE_PROVIDER env var.
        
        Returns:
            Configured Image provider instance
        """
        name = provider_name or os.getenv("IMAGE_PROVIDER", "fibo")
        provider_class = cls._image_providers.get(name.lower())
        
        if not provider_class:
            raise ValueError(
                f"Unknown Image provider: {name}. "
                f"Available: {list(cls._image_providers.keys())}"
            )
        
        return provider_class()
    
    # ============================================================
    # TEXT-TO-SPEECH PROVIDERS
    # ============================================================
    
    _tts_providers = {
        "gcp": GCPTTSProvider,
        "azure": AzureTTSProvider,
    }
    
    @classmethod
    def get_tts_provider(cls, provider_name: Optional[str] = None) -> BaseTTSProvider:
        """
        Get Text-to-Speech provider instance.
        
        Args:
            provider_name: Override provider (optional).
                          If None, uses VOICE_TTS_PROVIDER env var.
        
        Returns:
            Configured TTS provider instance
        """
        name = provider_name or os.getenv("VOICE_TTS_PROVIDER", "gcp")
        provider_class = cls._tts_providers.get(name.lower())
        
        if not provider_class:
            raise ValueError(
                f"Unknown TTS provider: {name}. "
                f"Available: {list(cls._tts_providers.keys())}"
            )
        
        return provider_class()
    
    # ============================================================
    # SPEECH-TO-TEXT PROVIDERS
    # ============================================================
    
    _stt_providers = {
        "gcp": GCPSTTProvider,
        "azure": AzureSTTProvider,
    }
    
    @classmethod
    def get_stt_provider(cls, provider_name: Optional[str] = None) -> BaseSTTProvider:
        """
        Get Speech-to-Text provider instance.
        
        Args:
            provider_name: Override provider (optional).
                          If None, uses VOICE_STT_PROVIDER env var.
        
        Returns:
            Configured STT provider instance
        """
        name = provider_name or os.getenv("VOICE_STT_PROVIDER", "gcp")
        provider_class = cls._stt_providers.get(name.lower())
        
        if not provider_class:
            raise ValueError(
                f"Unknown STT provider: {name}. "
                f"Available: {list(cls._stt_providers.keys())}"
            )
        
        return provider_class()
    
    # ============================================================
    # CONVENIENCE METHOD - GET ALL PROVIDERS
    # ============================================================
    
    @classmethod
    def get_all_providers(cls) -> dict:
        """
        Get all provider instances at once.
        
        Returns:
            Dictionary with all provider instances
        """
        return {
            "ai": cls.get_ai_provider(),
            "image": cls.get_image_provider(),
            "tts": cls.get_tts_provider(),
            "stt": cls.get_stt_provider(),
        }
    
    # ============================================================
    # PROVIDER HEALTH CHECK
    # ============================================================
    
    @classmethod
    async def check_all_providers(cls) -> dict:
        """
        Check health/connectivity of all configured providers.
        
        Returns:
            Dictionary with provider status
        """
        providers = cls.get_all_providers()
        status = {}
        
        for name, provider in providers.items():
            try:
                is_healthy = await provider.health_check()
                status[name] = {
                    "provider": provider.__class__.__name__,
                    "status": "healthy" if is_healthy else "unhealthy"
                }
            except Exception as e:
                status[name] = {
                    "provider": provider.__class__.__name__,
                    "status": "error",
                    "error": str(e)
                }
        
        return status
```

---

## BASE PROVIDER INTERFACES

### Create `backend/app/services/ai_providers/base.py`:

```python
"""
Base AI Provider Interface

All AI providers must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ContentGenerationRequest(BaseModel):
    topic: str
    difficulty_level: int  # 1-10
    visual_style: str  # "cartoon" or "realistic"
    num_images: int = 3
    avatar_description: Optional[str] = None
    character_descriptions: Optional[List[str]] = None


class QuestionGenerationRequest(BaseModel):
    topic: str
    difficulty_level: int
    content_context: str  # The story/content that was shown
    num_mcq: int = 3
    num_descriptive: int = 3


class AnswerEvaluationRequest(BaseModel):
    question: str
    model_answer: str
    user_answer: str
    keywords: List[str]
    max_score: int = 10


class BaseAIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def generate_content(
        self, 
        request: ContentGenerationRequest
    ) -> Dict[str, Any]:
        """
        Generate learning content including story narratives and facts.
        
        Returns:
            {
                "story_segments": [
                    {"narrative": "...", "facts": ["...", "..."], "image_prompt": "..."},
                    ...
                ],
                "topic_summary": "..."
            }
        """
        pass
    
    @abstractmethod
    async def generate_mcq_questions(
        self, 
        request: QuestionGenerationRequest
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple choice questions.
        
        Returns:
            [
                {
                    "question": "...",
                    "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
                    "correct_answer": "B",
                    "explanation": "..."
                },
                ...
            ]
        """
        pass
    
    @abstractmethod
    async def generate_descriptive_questions(
        self, 
        request: QuestionGenerationRequest
    ) -> List[Dict[str, Any]]:
        """
        Generate descriptive/open-ended questions.
        
        Returns:
            [
                {
                    "question": "...",
                    "model_answer": "...",
                    "keywords": ["...", "..."],
                    "max_score": 10
                },
                ...
            ]
        """
        pass
    
    @abstractmethod
    async def evaluate_answer(
        self, 
        request: AnswerEvaluationRequest
    ) -> Dict[str, Any]:
        """
        Evaluate a descriptive answer.
        
        Returns:
            {
                "score": 8,
                "max_score": 10,
                "feedback": {
                    "correct_points": ["...", "..."],
                    "improvements": ["...", "..."],
                    "explanation": "..."
                }
            }
        """
        pass
    
    @abstractmethod
    async def chat(
        self, 
        message: str, 
        context: Optional[str] = None,
        language: str = "en"
    ) -> str:
        """
        General chat/conversation capability.
        
        Returns:
            Response text
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass
```

### Create `backend/app/services/image_providers/base.py`:

```python
"""
Base Image Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel


class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str = "cartoon"  # "cartoon" or "realistic"
    width: int = 1024
    height: int = 576  # 16:9 aspect ratio
    avatar_image_path: Optional[str] = None
    character_image_paths: Optional[List[str]] = None


class BaseImageProvider(ABC):
    """Abstract base class for Image providers."""
    
    @abstractmethod
    async def generate_image(
        self, 
        request: ImageGenerationRequest
    ) -> bytes:
        """
        Generate an image based on prompt.
        
        Returns:
            Image bytes (PNG format)
        """
        pass
    
    @abstractmethod
    async def generate_avatar(
        self, 
        source_image: bytes,
        style: str = "cartoon"
    ) -> bytes:
        """
        Generate avatar from source image (upload or drawing).
        
        Returns:
            Avatar image bytes
        """
        pass
    
    @abstractmethod
    async def stylize_character(
        self, 
        source_image: bytes,
        style: str = "cartoon"
    ) -> bytes:
        """
        Convert uploaded image or drawing to character.
        
        Returns:
            Stylized character image bytes
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass
```

### Create `backend/app/services/voice_providers/base.py`:

```python
"""
Base Voice Provider Interfaces
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseTTSProvider(ABC):
    """Abstract base class for Text-to-Speech providers."""
    
    @abstractmethod
    async def synthesize_speech(
        self, 
        text: str,
        language: str = "en",
        voice_type: str = "female",  # "male" or "female"
        speed: float = 1.0
    ) -> bytes:
        """
        Convert text to speech audio.
        
        Returns:
            Audio bytes (MP3 format)
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass


class BaseSTTProvider(ABC):
    """Abstract base class for Speech-to-Text providers."""
    
    @abstractmethod
    async def transcribe_audio(
        self, 
        audio_data: bytes,
        language: str = "en",
        audio_format: str = "wav"
    ) -> str:
        """
        Convert speech audio to text.
        
        Returns:
            Transcribed text
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        pass
```

---

## GEMINI 3 PROVIDER IMPLEMENTATION

### Create `backend/app/services/ai_providers/gemini.py`:

```python
"""
Google Gemini 3 AI Provider Implementation
"""

import os
import json
import httpx
from typing import List, Dict, Any, Optional
from .base import (
    BaseAIProvider, 
    ContentGenerationRequest,
    QuestionGenerationRequest,
    AnswerEvaluationRequest
)


class GeminiProvider(BaseAIProvider):
    """Gemini 3 implementation of AI provider."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
    
    async def _call_api(self, prompt: str, system_instruction: str = "") -> str:
        """Make API call to Gemini."""
        url = f"{self.base_url}/models/{self.model}:generateContent"
        
        headers = {
            "Content-Type": "application/json",
        }
        
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            }
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    
    async def generate_content(
        self, 
        request: ContentGenerationRequest
    ) -> Dict[str, Any]:
        """Generate learning content with story narratives."""
        
        system_instruction = """You are an expert educational content creator. 
        Create engaging, age-appropriate learning content with storytelling elements.
        Always respond with valid JSON only, no markdown formatting."""
        
        avatar_context = ""
        if request.avatar_description:
            avatar_context = f"Include a character named after the learner's avatar: {request.avatar_description}. "
        
        character_context = ""
        if request.character_descriptions:
            chars = ", ".join(request.character_descriptions)
            character_context = f"Also include these characters in the story: {chars}. "
        
        prompt = f"""Create educational content about "{request.topic}" for difficulty level {request.difficulty_level}/10.

{avatar_context}{character_context}

Generate exactly {request.num_images} story segments in {request.visual_style} style.

Respond with ONLY this JSON structure (no markdown, no code blocks):
{{
    "story_segments": [
        {{
            "segment_number": 1,
            "narrative": "A short engaging story paragraph (2-3 sentences)",
            "facts": ["Fact 1 about the topic", "Fact 2 about the topic"],
            "image_prompt": "Detailed prompt for {request.visual_style} style image generation including characters and scene"
        }}
    ],
    "topic_summary": "Brief summary of what was covered"
}}"""
        
        response_text = await self._call_api(prompt, system_instruction)
        
        # Clean response and parse JSON
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text)
    
    async def generate_mcq_questions(
        self, 
        request: QuestionGenerationRequest
    ) -> List[Dict[str, Any]]:
        """Generate MCQ questions based on content."""
        
        system_instruction = """You are an expert quiz creator.
        Create challenging but fair multiple choice questions.
        Always respond with valid JSON only, no markdown formatting."""
        
        prompt = f"""Based on this learning content about "{request.topic}":

{request.content_context}

Create exactly {request.num_mcq} multiple choice questions at difficulty level {request.difficulty_level}/10.

Respond with ONLY this JSON array (no markdown, no code blocks):
[
    {{
        "question": "Clear question text?",
        "options": {{
            "A": "First option",
            "B": "Second option",
            "C": "Third option",
            "D": "Fourth option"
        }},
        "correct_answer": "B",
        "explanation": "Why B is correct and others are wrong"
    }}
]"""
        
        response_text = await self._call_api(prompt, system_instruction)
        
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text)
    
    async def generate_descriptive_questions(
        self, 
        request: QuestionGenerationRequest
    ) -> List[Dict[str, Any]]:
        """Generate descriptive questions."""
        
        system_instruction = """You are an expert assessment creator.
        Create open-ended questions that test deep understanding.
        Always respond with valid JSON only, no markdown formatting."""
        
        prompt = f"""Based on this learning content about "{request.topic}":

{request.content_context}

Create exactly {request.num_descriptive} descriptive questions at difficulty level {request.difficulty_level}/10.

Respond with ONLY this JSON array (no markdown, no code blocks):
[
    {{
        "question": "Open-ended question requiring explanation?",
        "model_answer": "Comprehensive model answer (3-5 sentences)",
        "keywords": ["key", "terms", "expected", "in", "answer"],
        "max_score": 10
    }}
]"""
        
        response_text = await self._call_api(prompt, system_instruction)
        
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text)
    
    async def evaluate_answer(
        self, 
        request: AnswerEvaluationRequest
    ) -> Dict[str, Any]:
        """Evaluate a descriptive answer using AI."""
        
        system_instruction = """You are an expert educational evaluator.
        Provide fair, constructive feedback on student answers.
        Always respond with valid JSON only, no markdown formatting."""
        
        prompt = f"""Evaluate this student answer:

Question: {request.question}

Model Answer: {request.model_answer}

Expected Keywords: {', '.join(request.keywords)}

Student's Answer: {request.user_answer}

Maximum Score: {request.max_score}

Evaluate fairly and respond with ONLY this JSON (no markdown, no code blocks):
{{
    "score": <number between 0 and {request.max_score}>,
    "max_score": {request.max_score},
    "feedback": {{
        "correct_points": ["Points the student got right"],
        "improvements": ["Areas that could be improved"],
        "explanation": "Detailed explanation of the score"
    }}
}}"""
        
        response_text = await self._call_api(prompt, system_instruction)
        
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text)
    
    async def chat(
        self, 
        message: str, 
        context: Optional[str] = None,
        language: str = "en"
    ) -> str:
        """General chat capability."""
        
        language_instruction = ""
        if language != "en":
            language_instruction = f"Respond in the language with code: {language}. "
        
        system_instruction = f"""You are a helpful AI learning assistant.
        {language_instruction}
        Be encouraging, clear, and educational in your responses."""
        
        prompt = message
        if context:
            prompt = f"Context: {context}\n\nUser message: {message}"
        
        return await self._call_api(prompt, system_instruction)
    
    async def health_check(self) -> bool:
        """Check if Gemini API is accessible."""
        try:
            await self._call_api("Say 'OK' if you can read this.")
            return True
        except Exception:
            return False
```

---

## MAIN FASTAPI APPLICATION

### Create `backend/app/main.py`:

```python
"""
GenLearn AI - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.api.routes import (
    auth,
    users,
    learning,
    avatar,
    characters,
    quiz,
    voice,
    video,
    tournaments,
    teams,
    admin,
    chat
)
from app.services.provider_factory import ProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    print("🚀 Starting GenLearn AI...")
    print(f"📦 AI Provider: {os.getenv('AI_PROVIDER', 'gemini')}")
    print(f"🖼️  Image Provider: {os.getenv('IMAGE_PROVIDER', 'fibo')}")
    print(f"🔊 TTS Provider: {os.getenv('VOICE_TTS_PROVIDER', 'gcp')}")
    print(f"🎤 STT Provider: {os.getenv('VOICE_STT_PROVIDER', 'gcp')}")
    
    # Check provider health
    try:
        status = await ProviderFactory.check_all_providers()
        for name, info in status.items():
            emoji = "✅" if info["status"] == "healthy" else "❌"
            print(f"  {emoji} {name}: {info['provider']} - {info['status']}")
    except Exception as e:
        print(f"  ⚠️ Provider health check failed: {e}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down GenLearn AI...")


app = FastAPI(
    title="GenLearn AI",
    description="Generative AI-Enabled Adaptive Learning System",
    version="1.0.0-prototype",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for media
app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(avatar.router, prefix="/api/avatar", tags=["Avatar"])
app.include_router(characters.router, prefix="/api/characters", tags=["Characters"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])
app.include_router(video.router, prefix="/api/video", tags=["Video"])
app.include_router(tournaments.router, prefix="/api/tournaments", tags=["Tournaments"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to GenLearn AI",
        "version": "1.0.0-prototype",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    providers = await ProviderFactory.check_all_providers()
    return {
        "status": "healthy",
        "providers": providers
    }
```

---

## FRONTEND API SERVICE

### Create `frontend/src/services/api.ts`:

```typescript
/**
 * API Service - Centralized API communication layer
 * 
 * All API calls go through this service.
 * Base URL and authentication are handled here.
 */

import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor - add auth token
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // ============================================================
  // AUTHENTICATION
  // ============================================================

  async login(username: string, password: string) {
    const response = await this.client.post('/auth/login', { username, password });
    return response.data;
  }

  async logout() {
    localStorage.removeItem('auth_token');
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // ============================================================
  // LEARNING
  // ============================================================

  async startSession(config: {
    topic: string;
    difficulty_level: number;
    duration_minutes: number;
    visual_style: 'cartoon' | 'realistic';
    play_mode: 'solo' | 'team' | 'tournament';
    team_id?: string;
    tournament_id?: string;
  }) {
    const response = await this.client.post('/learning/start', config);
    return response.data;
  }

  async getSessionContent(sessionId: string) {
    const response = await this.client.get(`/learning/session/${sessionId}/content`);
    return response.data;
  }

  async submitProgress(sessionId: string, data: any) {
    const response = await this.client.post(`/learning/session/${sessionId}/progress`, data);
    return response.data;
  }

  async endSession(sessionId: string) {
    const response = await this.client.post(`/learning/session/${sessionId}/end`);
    return response.data;
  }

  // ============================================================
  // QUIZ
  // ============================================================

  async getMCQQuestions(sessionId: string) {
    const response = await this.client.get(`/quiz/session/${sessionId}/mcq`);
    return response.data;
  }

  async submitMCQAnswer(sessionId: string, questionId: string, answer: string) {
    const response = await this.client.post(`/quiz/session/${sessionId}/mcq/answer`, {
      question_id: questionId,
      answer,
    });
    return response.data;
  }

  async getDescriptiveQuestions(sessionId: string) {
    const response = await this.client.get(`/quiz/session/${sessionId}/descriptive`);
    return response.data;
  }

  async submitDescriptiveAnswer(sessionId: string, questionId: string, answer: string) {
    const response = await this.client.post(`/quiz/session/${sessionId}/descriptive/answer`, {
      question_id: questionId,
      answer,
    });
    return response.data;
  }

  // ============================================================
  // AVATAR & CHARACTERS
  // ============================================================

  async getAvatars() {
    const response = await this.client.get('/avatar/list');
    return response.data;
  }

  async createAvatarFromUpload(file: File, name: string, style: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('style', style);
    const response = await this.client.post('/avatar/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async createAvatarFromDrawing(drawingData: string, name: string, style: string) {
    const response = await this.client.post('/avatar/draw', {
      drawing_data: drawingData,
      name,
      style,
    });
    return response.data;
  }

  async getCharacters() {
    const response = await this.client.get('/characters/list');
    return response.data;
  }

  async createCharacter(file: File, name: string, description: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('description', description);
    const response = await this.client.post('/characters/create', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  // ============================================================
  // VOICE
  // ============================================================

  async textToSpeech(text: string, language: string, voiceType: string) {
    const response = await this.client.post('/voice/tts', {
      text,
      language,
      voice_type: voiceType,
    }, { responseType: 'blob' });
    return response.data;
  }

  async speechToText(audioBlob: Blob, language: string) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    formData.append('language', language);
    const response = await this.client.post('/voice/stt', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  // ============================================================
  // VIDEO
  // ============================================================

  async getVideo(sessionId: string, cycleNumber: number) {
    const response = await this.client.get(`/video/session/${sessionId}/cycle/${cycleNumber}`);
    return response.data;
  }

  async checkVideoStatus(sessionId: string, cycleNumber: number) {
    const response = await this.client.get(`/video/session/${sessionId}/cycle/${cycleNumber}/status`);
    return response.data;
  }

  // ============================================================
  // TOURNAMENTS & TEAMS
  // ============================================================

  async getTournaments(status?: string) {
    const params = status ? { status } : {};
    const response = await this.client.get('/tournaments/list', { params });
    return response.data;
  }

  async joinTournament(tournamentId: string, teamId?: string) {
    const response = await this.client.post(`/tournaments/${tournamentId}/join`, { team_id: teamId });
    return response.data;
  }

  async getTeams() {
    const response = await this.client.get('/teams/list');
    return response.data;
  }

  async createTeam(name: string) {
    const response = await this.client.post('/teams/create', { name });
    return response.data;
  }

  async joinTeam(teamId: string) {
    const response = await this.client.post(`/teams/${teamId}/join`);
    return response.data;
  }

  async getLeaderboard(scope?: 'global' | 'tournament', tournamentId?: string) {
    const params: any = {};
    if (scope) params.scope = scope;
    if (tournamentId) params.tournament_id = tournamentId;
    const response = await this.client.get('/tournaments/leaderboard', { params });
    return response.data;
  }

  // ============================================================
  // CHAT
  // ============================================================

  async sendChatMessage(message: string, context?: string, language?: string) {
    const response = await this.client.post('/chat/message', {
      message,
      context,
      language,
    });
    return response.data;
  }

  // ============================================================
  // ADMIN
  // ============================================================

  async createTournament(data: any) {
    const response = await this.client.post('/admin/tournaments/create', data);
    return response.data;
  }

  async uploadQuestions(file: File, questionType: 'mcq' | 'descriptive') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question_type', questionType);
    const response = await this.client.post('/admin/questions/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async getUsers() {
    const response = await this.client.get('/admin/users');
    return response.data;
  }

  // ============================================================
  // HISTORY & PROFILE
  // ============================================================

  async getLearningHistory() {
    const response = await this.client.get('/users/history');
    return response.data;
  }

  async updateProfile(data: any) {
    const response = await this.client.put('/users/profile', data);
    return response.data;
  }

  async updateSettings(data: any) {
    const response = await this.client.put('/users/settings', data);
    return response.data;
  }
}

export const api = new ApiService();
export default api;
```

---

## TYPESCRIPT TYPES

### Create `frontend/src/types/index.ts`:

```typescript
/**
 * TypeScript type definitions for GenLearn AI
 */

// ============================================================
// USER TYPES
// ============================================================

export interface User {
  user_id: string;
  username: string;
  email: string;
  role: 'admin' | 'user';
  display_name: string;
  avatar_id?: string;
  language_preference: string;
  voice_preference: 'male' | 'female';
  full_vocal_mode: boolean;
  xp_points: number;
  level: number;
  streak_days: number;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// ============================================================
// LEARNING TYPES
// ============================================================

export interface CourseConfig {
  topic: string;
  difficulty_level: number;
  duration_minutes: number;
  visual_style: 'cartoon' | 'realistic';
  play_mode: 'solo' | 'team' | 'tournament';
  team_id?: string;
  tournament_id?: string;
}

export interface LearningSession {
  session_id: string;
  user_id: string;
  topic: string;
  difficulty_level: number;
  duration_minutes: number;
  visual_style: 'cartoon' | 'realistic';
  play_mode: 'solo' | 'team' | 'tournament';
  status: 'in_progress' | 'completed' | 'abandoned';
  current_cycle: number;
  total_cycles: number;
  score: number;
}

export interface StorySegment {
  segment_number: number;
  narrative: string;
  facts: string[];
  image_url: string;
  audio_url?: string;
}

export interface LearningContent {
  session_id: string;
  story_segments: StorySegment[];
  topic_summary: string;
}

// ============================================================
// QUIZ TYPES
// ============================================================

export interface MCQQuestion {
  question_id: string;
  question_text: string;
  options: {
    A: string;
    B: string;
    C: string;
    D: string;
  };
  image_url?: string;
}

export interface MCQAnswer {
  question_id: string;
  selected_answer: string;
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
  points_earned: number;
}

export interface DescriptiveQuestion {
  question_id: string;
  question_text: string;
  max_score: number;
}

export interface DescriptiveAnswer {
  question_id: string;
  score: number;
  max_score: number;
  feedback: {
    correct_points: string[];
    improvements: string[];
    explanation: string;
  };
}

// ============================================================
// AVATAR & CHARACTER TYPES
// ============================================================

export interface Avatar {
  avatar_id: string;
  user_id: string;
  name: string;
  image_url: string;
  creation_method: 'draw' | 'upload' | 'gallery';
  style: 'cartoon' | 'realistic';
}

export interface Character {
  character_id: string;
  user_id: string;
  name: string;
  image_url: string;
  creation_method: 'draw' | 'upload' | 'gallery';
  description: string;
}

// ============================================================
// GAMIFICATION TYPES
// ============================================================

export interface Tournament {
  tournament_id: string;
  name: string;
  topic: string;
  difficulty_level: number;
  start_datetime: string;
  end_datetime: string;
  duration_minutes: number;
  max_participants: number;
  current_participants: number;
  status: 'upcoming' | 'active' | 'completed';
  entry_type: 'free' | 'invite_only';
  prizes: {
    first: string;
    second: string;
    third: string;
  };
}

export interface Team {
  team_id: string;
  team_name: string;
  created_by: string;
  total_score: number;
  rank: number;
  members: TeamMember[];
}

export interface TeamMember {
  user_id: string;
  display_name: string;
  role: 'leader' | 'member';
  avatar_url?: string;
}

export interface LeaderboardEntry {
  rank: number;
  user_id?: string;
  team_id?: string;
  display_name: string;
  score: number;
  avatar_url?: string;
}

// ============================================================
// VOICE TYPES
// ============================================================

export interface VoiceSettings {
  language: string;
  voice_type: 'male' | 'female';
  speed: number;
  full_vocal_mode: boolean;
}

// ============================================================
// VIDEO TYPES
// ============================================================

export interface VideoStatus {
  session_id: string;
  cycle_number: number;
  status: 'generating' | 'ready' | 'failed';
  video_url?: string;
  progress_percent?: number;
}
```

---

## KEY IMPLEMENTATION NOTES

### 1. CSV Database Handler

Create a robust CSV handler in `backend/app/database/csv_handler.py` that:
- Uses pandas for reading/writing CSV files
- Implements CRUD operations (Create, Read, Update, Delete)
- Handles file locking for concurrent access
- Auto-generates unique IDs (e.g., USR007, SES015)

### 2. File Handler for Media

Create `backend/app/database/file_handler.py` that:
- Manages file uploads to appropriate folders
- Generates unique filenames
- Returns file paths and URLs
- Handles image/video/audio files

### 3. Full Vocal Mode Implementation

Frontend implementation should:
- Use Web Speech API for continuous listening
- Maintain a voice command vocabulary
- Provide audio feedback for all actions
- Support keyboard shortcuts (Ctrl+Shift+V toggle)

### 4. Video Generation Pipeline

Backend should:
- Generate video asynchronously (background task)
- Use FFmpeg to compose images with audio
- Save to `data/media/generated_videos/`
- Implement status polling endpoint

### 5. Authentication Flow

- Simple JWT-based authentication
- Password hashing with bcrypt
- Token stored in localStorage
- Auto-refresh on 401 errors

---

## RUNNING THE APPLICATION

### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

### Default Login Credentials:
- **Admin**: username: `admin`, password: `password123`
- **User**: username: `john_doe`, password: `password123`

---

## SUMMARY OF SWITCHING PROVIDERS

To switch any provider, simply change the environment variable in `.env`:

| What to Change | Environment Variable | Options |
|----------------|---------------------|---------|
| AI/LLM Provider | `AI_PROVIDER` | `gemini`, `openai`, `anthropic` |
| Image Generation | `IMAGE_PROVIDER` | `fibo`, `stability` |
| Text-to-Speech | `VOICE_TTS_PROVIDER` | `gcp`, `azure` |
| Speech-to-Text | `VOICE_STT_PROVIDER` | `gcp`, `azure` |

**No code changes required!** The `ProviderFactory` handles everything automatically.

---

## FINAL CHECKLIST

Ensure all these features are implemented:

- [ ] Three-panel layout (Left Menu, Main Content, Right Panel)
- [ ] Login/Authentication with admin and user roles
- [ ] Course setup with topic, difficulty, duration, visual style
- [ ] 3-image story carousel with facts and narratives
- [ ] MCQ quiz with visual backgrounds
- [ ] Descriptive questions with AI evaluation
- [ ] 8-second video generation (background process)
- [ ] Avatar creation (draw, upload, gallery)
- [ ] Character management
- [ ] Voice input (mic button) and output (audio button)
- [ ] Full Vocal Mode for accessibility
- [ ] Multilingual support
- [ ] Team and solo play modes
- [ ] Tournament system with admin management
- [ ] Scoreboard and leaderboard
- [ ] Admin dashboard for content upload
- [ ] CSV file question upload (MCQ and descriptive)
- [ ] Adaptive content scaling based on duration
- [ ] Learning history tracking

---

Build this complete prototype following all specifications above. Create all files, implement all features, and ensure the application runs successfully with the sample data provided.
