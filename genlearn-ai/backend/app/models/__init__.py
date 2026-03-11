"""
Models package - Pydantic models for R U Serious?
"""

from .user import (
    User,
    UserCreate,
    UserUpdate,
    UserProfile,
    UserStats,
    UserSettings,
    UserPasswordUpdate
)
from .session import (
    LearningSession,
    SessionCreate,
    SessionProgress,
    SessionEnd,
    SessionContent,
    SessionSummary,
    StorySegment,
    LearningHistory
)
from .quiz import (
    MCQQuestion,
    MCQQuestionCreate,
    MCQQuestionDisplay,
    MCQAnswerSubmit,
    MCQAnswerResult,
    DescriptiveQuestion,
    DescriptiveQuestionCreate,
    DescriptiveQuestionDisplay,
    DescriptiveAnswerSubmit,
    DescriptiveAnswerResult,
    Answer,
    QuizResults,
    AnswerFeedback
)
from .tournament import (
    Tournament,
    TournamentCreate,
    TournamentUpdate,
    TournamentParticipant,
    TournamentJoin,
    TournamentLeaderboard,
    TournamentResults,
    TournamentStats
)
from .team import (
    Team,
    TeamCreate,
    TeamUpdate,
    TeamMember,
    TeamMemberCreate,
    TeamMemberInfo,
    TeamDetails,
    TeamStats,
    TeamLeaderboard,
    TeamInvite,
    TeamJoinRequest
)
from .avatar import (
    Avatar,
    AvatarCreate,
    AvatarUpdate,
    AvatarDisplay,
    Character,
    CharacterCreate,
    CharacterUpdate,
    CharacterDisplay,
    DrawingData,
    ImageUpload
)

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserUpdate",
    "UserProfile",
    "UserStats",
    "UserSettings",
    "UserPasswordUpdate",
    # Session models
    "LearningSession",
    "SessionCreate",
    "SessionProgress",
    "SessionEnd",
    "SessionContent",
    "SessionSummary",
    "StorySegment",
    "LearningHistory",
    # Quiz models
    "MCQQuestion",
    "MCQQuestionCreate",
    "MCQQuestionDisplay",
    "MCQAnswerSubmit",
    "MCQAnswerResult",
    "DescriptiveQuestion",
    "DescriptiveQuestionCreate",
    "DescriptiveQuestionDisplay",
    "DescriptiveAnswerSubmit",
    "DescriptiveAnswerResult",
    "Answer",
    "QuizResults",
    "AnswerFeedback",
    # Tournament models
    "Tournament",
    "TournamentCreate",
    "TournamentUpdate",
    "TournamentParticipant",
    "TournamentJoin",
    "TournamentLeaderboard",
    "TournamentResults",
    "TournamentStats",
    # Team models
    "Team",
    "TeamCreate",
    "TeamUpdate",
    "TeamMember",
    "TeamMemberCreate",
    "TeamMemberInfo",
    "TeamDetails",
    "TeamStats",
    "TeamLeaderboard",
    "TeamInvite",
    "TeamJoinRequest",
    # Avatar models
    "Avatar",
    "AvatarCreate",
    "AvatarUpdate",
    "AvatarDisplay",
    "Character",
    "CharacterCreate",
    "CharacterUpdate",
    "CharacterDisplay",
    "DrawingData",
    "ImageUpload",
]
