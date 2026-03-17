import React, { useState, useEffect } from 'react';
import { CourseConfig, Avatar, Character } from '../../types';
import { Button } from '../common/Button';
import { Dropdown } from '../common/Dropdown';
import { Slider } from '../common/Slider';
import { DIFFICULTY_LEVELS, DURATION_OPTIONS, VISUAL_STYLES, PLAY_MODES, STORY_STYLES } from '../../utils/constants';
import api, { BACKEND_URL } from '../../services/api';

interface CourseSetupProps {
  onStart: (config: CourseConfig) => void;
}

export const CourseSetup: React.FC<CourseSetupProps> = ({ onStart }) => {
  const [config, setConfig] = useState<CourseConfig>({
    topic: '',
    difficulty_level: 5,
    duration_minutes: 10,
    visual_style: 'cartoon',
    story_style: 'fun',
    play_mode: 'solo',
  });

  const [avatars, setAvatars] = useState<any[]>([]);
  const [characters, setCharacters] = useState<Character[]>([]);
  const [selectedCharacters, setSelectedCharacters] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Built-in default avatars from DiceBear
  const defaultAvatars = [
    { avatar_id: 'default-1', name: 'Felix', image_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix' },
    { avatar_id: 'default-2', name: 'Luna', image_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Luna' },
    { avatar_id: 'default-3', name: 'Max', image_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Max' },
    { avatar_id: 'default-4', name: 'Sophie', image_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sophie' },
    { avatar_id: 'default-5', name: 'Oliver', image_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Oliver' },
    { avatar_id: 'default-6', name: 'Emma', image_url: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Emma' },
    { avatar_id: 'default-7', name: 'Midnight', image_url: 'https://api.dicebear.com/7.x/adventurer/svg?seed=Midnight' },
    { avatar_id: 'default-8', name: 'Sunny', image_url: 'https://api.dicebear.com/7.x/adventurer/svg?seed=Sunny' },
    { avatar_id: 'default-9', name: 'Buster', image_url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Buster' },
    { avatar_id: 'default-10', name: 'Coco', image_url: 'https://api.dicebear.com/7.x/bottts/svg?seed=Coco' },
  ];

  useEffect(() => {
    loadUserAssets();
  }, []);

  const loadUserAssets = async () => {
    try {
      setIsLoading(true);
      const [avatarRes, characterRes] = await Promise.allSettled([
        api.get('/avatar/list'),
        api.get('/characters/list')
      ]);
      const backendAvatars = avatarRes.status === 'fulfilled' ? (avatarRes.value.data || []) : [];
      setAvatars([...defaultAvatars, ...backendAvatars]);
      setCharacters(characterRes.status === 'fulfilled' ? (characterRes.value.data || []) : []);
    } catch (err) {
      console.error('Failed to load assets:', err);
      setAvatars(defaultAvatars);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleCharacter = (characterId: string) => {
    setSelectedCharacters(prev => {
      if (prev.includes(characterId)) {
        return prev.filter(id => id !== characterId);
      }
      if (prev.length >= 3) {
        return prev; // Max 3 characters
      }
      return [...prev, characterId];
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onStart({
      ...config,
      character_ids: selectedCharacters.length > 0 ? selectedCharacters : undefined
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-8 max-w-4xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-900 mb-2">🎓 Configure Your Learning Adventure</h2>
      <p className="text-gray-600 mb-8">Customize your learning experience with story style, characters, and more!</p>

      <div className="space-y-8">
        {/* Topic Input */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            📚 What do you want to learn?
          </label>
          <input
            type="text"
            value={config.topic}
            onChange={(e) => setConfig({ ...config, topic: e.target.value })}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-lg"
            placeholder="e.g., Photosynthesis, Python Basics, World War II, Solar System"
            required
          />
        </div>

        {/* Story Style Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            🎭 Choose Your Story Style
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {STORY_STYLES.map((style) => (
              <button
                key={style.value}
                type="button"
                onClick={() => setConfig({ ...config, story_style: style.value as any })}
                className={`p-4 border-2 rounded-xl transition-all text-left ${config.story_style === style.value
                    ? 'border-primary-600 bg-primary-50 shadow-md'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
              >
                <div className="text-2xl mb-1">{style.icon}</div>
                <div className="font-semibold text-gray-800">{style.label}</div>
                <div className="text-xs text-gray-500 mt-1">{style.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Avatar Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            👤 Select Your Avatar (Optional)
          </label>
          {isLoading ? (
            <div className="text-gray-500">Loading avatars...</div>
          ) : (
            <div className="flex gap-3 overflow-x-auto pb-2">
              {/* No avatar option */}
              <button
                type="button"
                onClick={() => setConfig({ ...config, avatar_id: undefined })}
                className={`flex-shrink-0 w-20 h-20 rounded-xl border-2 flex items-center justify-center transition-all ${!config.avatar_id
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                  }`}
              >
                <span className="text-gray-400 text-sm">None</span>
              </button>
              {avatars.map((avatar) => (
                <button
                  key={avatar.avatar_id}
                  type="button"
                  onClick={() => setConfig({ ...config, avatar_id: avatar.avatar_id })}
                  className={`flex-shrink-0 w-20 h-20 rounded-xl border-2 overflow-hidden transition-all ${config.avatar_id === avatar.avatar_id
                      ? 'border-primary-600 ring-2 ring-primary-300'
                      : 'border-gray-200 hover:border-gray-300'
                    }`}
                  title={avatar.name}
                >
                  <img
                    src={avatar.image_url.startsWith('http') ? avatar.image_url : `${BACKEND_URL}${avatar.image_url}`}
                    alt={avatar.name}
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Character Selection */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            🎭 Select Story Characters (Max 3)
          </label>
          {isLoading ? (
            <div className="text-gray-500">Loading characters...</div>
          ) : characters.length === 0 ? (
            <div className="bg-gray-50 rounded-xl p-4 text-center">
              <p className="text-gray-600">No characters yet!</p>
              <a href="/characters" className="text-primary-600 hover:underline text-sm">Create characters →</a>
            </div>
          ) : (
            <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {characters.map((character) => {
                const isSelected = selectedCharacters.includes(character.character_id);
                return (
                  <button
                    key={character.character_id}
                    type="button"
                    onClick={() => toggleCharacter(character.character_id)}
                    className={`relative rounded-xl border-2 overflow-hidden transition-all ${isSelected
                        ? 'border-primary-600 ring-2 ring-primary-300'
                        : 'border-gray-200 hover:border-gray-300'
                      }`}
                  >
                    <img
                      src={`${BACKEND_URL}${character.image_url}`}
                      alt={character.name}
                      className="w-full aspect-square object-cover"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23fef3c7" width="100" height="100"/><text x="50" y="55" text-anchor="middle" fill="%23d97706" font-size="40">🎭</text></svg>';
                      }}
                    />
                    <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-xs py-1 px-2 truncate">
                      {character.name}
                    </div>
                    {isSelected && (
                      <div className="absolute top-1 right-1 w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
                        <span className="text-white text-xs">✓</span>
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          )}
          {selectedCharacters.length > 0 && (
            <p className="text-sm text-gray-500 mt-2">
              {selectedCharacters.length}/3 characters selected
            </p>
          )}
        </div>

        {/* Difficulty and Duration Row */}
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <Slider
              label="⚡ Difficulty Level"
              value={config.difficulty_level}
              onChange={(value) => setConfig({ ...config, difficulty_level: value })}
              min={1}
              max={10}
              step={1}
            />
            <p className="text-sm text-gray-500 mt-1">
              {DIFFICULTY_LEVELS.find(d => d.value === config.difficulty_level)?.label}
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              ⏱️ Duration
            </label>
            <Dropdown
              options={DURATION_OPTIONS}
              value={config.duration_minutes}
              onChange={(value) => setConfig({ ...config, duration_minutes: Number(value) })}
            />
            <p className="text-sm text-gray-500 mt-1">
              {config.duration_minutes} questions will be asked
            </p>
          </div>
        </div>

        {/* Visual Style */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            🎨 Visual Style
          </label>
          <div className="grid grid-cols-2 gap-4">
            {VISUAL_STYLES.map((style) => (
              <button
                key={style.value}
                type="button"
                onClick={() => setConfig({ ...config, visual_style: style.value as any })}
                className={`p-4 border-2 rounded-xl transition-all ${config.visual_style === style.value
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                  }`}
              >
                <div className="text-xl mb-1">{style.value === 'cartoon' ? '🎨' : '📸'}</div>
                <div className="font-medium">{style.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Play Mode */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            🎮 Play Mode
          </label>
          <div className="grid grid-cols-3 gap-4">
            {PLAY_MODES.map((mode) => (
              <button
                key={mode.value}
                type="button"
                onClick={() => setConfig({ ...config, play_mode: mode.value as any })}
                className={`p-4 border-2 rounded-xl transition-all ${config.play_mode === mode.value
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                  }`}
              >
                <div className="text-2xl mb-2">{mode.icon}</div>
                <div className="text-sm font-medium">{mode.label}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Submit Button */}
        <Button type="submit" variant="primary" size="lg" className="w-full text-lg py-4">
          🚀 Start Learning Adventure
        </Button>
      </div>
    </form>
  );
};
