/**
 * Application constants
 */

export const APP_NAME = 'R U Serious?';

export const DIFFICULTY_LEVELS = [
  { value: 1, label: 'Very Easy' },
  { value: 2, label: 'Easy' },
  { value: 3, label: 'Easy-Medium' },
  { value: 4, label: 'Medium' },
  { value: 5, label: 'Medium-Hard' },
  { value: 6, label: 'Hard' },
  { value: 7, label: 'Hard-Very Hard' },
  { value: 8, label: 'Very Hard' },
  { value: 9, label: 'Expert' },
  { value: 10, label: 'Master' },
];

export const DURATION_OPTIONS = [
  { value: 5, label: '5 minutes' },
  { value: 10, label: '10 minutes' },
  { value: 15, label: '15 minutes' },
  { value: 20, label: '20 minutes' },
  { value: 30, label: '30 minutes' },
];

export const VISUAL_STYLES = [
  { value: 'cartoon', label: 'Cartoon' },
  { value: 'realistic', label: 'Realistic' },
];

export const PLAY_MODES = [
  { value: 'solo', label: 'Solo Play', icon: '👤' },
  { value: 'team', label: 'Team Play', icon: '👥' },
  { value: 'tournament', label: 'Tournament', icon: '🏆' },
];

export const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'bn', name: 'Bengali', flag: '🇧🇩' },
  { code: 'te', name: 'Telugu', flag: '🇮🇳' },
  { code: 'mr', name: 'Marathi', flag: '🇮🇳' },
  { code: 'ta', name: 'Tamil', flag: '🇮🇳' },
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
];

export const VOICE_TYPES = [
  { value: 'male', label: 'Male Voice' },
  { value: 'female', label: 'Female Voice' },
];

export const XP_PER_LEVEL = 500;

export const POINTS = {
  MCQ_CORRECT: 10,
  MCQ_INCORRECT: 2,
  DESCRIPTIVE_MAX: 10,
  STREAK_BONUS: 50,
};

export const STORY_STYLES = [
  { value: 'thriller', label: 'Thriller', icon: '🔪', description: 'Suspenseful and edge-of-your-seat' },
  { value: 'fun', label: 'Fun', icon: '🎉', description: 'Light-hearted and entertaining' },
  { value: 'nostalgic', label: 'Nostalgic', icon: '📜', description: 'Warm memories and classic vibes' },
  { value: 'adventure', label: 'Adventure', icon: '🗺️', description: 'Epic journeys and discoveries' },
  { value: 'mystery', label: 'Mystery', icon: '🔍', description: 'Clues, puzzles, and revelations' },
  { value: 'scifi', label: 'Sci-Fi', icon: '🚀', description: 'Futuristic and technological' },
];
