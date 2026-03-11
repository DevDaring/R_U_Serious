/**
 * TypeScript type definitions for R U Serious?
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
  story_style: 'thriller' | 'fun' | 'nostalgic' | 'adventure' | 'mystery' | 'scifi';
  play_mode: 'solo' | 'team' | 'tournament';
  avatar_id?: string;
  character_ids?: string[];
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

// ============================================================
// CHAT TYPES
// ============================================================

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

// ============================================================
// HISTORY TYPES
// ============================================================

export interface LearningHistoryItem {
  history_id: string;
  session_id: string;
  content_type: 'image' | 'video' | 'quiz';
  topic: string;
  score?: number;
  viewed_at: string;
}
