import React from 'react';
import { useSettingsStore } from '../store/settingsStore';
import { LANGUAGES, VOICE_TYPES } from '../utils/constants';
import { Dropdown } from '../components/common/Dropdown';
import { Slider } from '../components/common/Slider';

export const SettingsPage: React.FC = () => {
  const {
    language,
    voiceType,
    voiceSpeed,
    fullVocalMode,
    setLanguage,
    setVoiceType,
    setVoiceSpeed,
    toggleFullVocalMode,
  } = useSettingsStore();

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h1 className="text-3xl font-bold mb-6">Settings</h1>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Language
            </label>
            <Dropdown
              options={LANGUAGES.map(lang => ({ value: lang.code, label: `${lang.flag} ${lang.name}` }))}
              value={language}
              onChange={(value) => setLanguage(value as string)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Voice Type
            </label>
            <Dropdown
              options={VOICE_TYPES}
              value={voiceType}
              onChange={(value) => setVoiceType(value as 'male' | 'female')}
            />
          </div>

          <div>
            <Slider
              label="Voice Speed"
              value={voiceSpeed}
              onChange={setVoiceSpeed}
              min={0.5}
              max={2}
              step={0.1}
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Full Vocal Mode</h3>
              <p className="text-sm text-gray-600">Enable hands-free voice-controlled learning</p>
            </div>
            <button
              onClick={toggleFullVocalMode}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                fullVocalMode ? 'bg-primary-600' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  fullVocalMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
