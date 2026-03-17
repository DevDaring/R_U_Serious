import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Character } from '../types';

const BACKEND_URL = import.meta.env.VITE_API_URL?.replace('/api', '') || '';

export const CharacterPage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  useEffect(() => {
    loadCharacters();
  }, []);

  const loadCharacters = async () => {
    try {
      const res = await api.getCharacters();
      setCharacters(Array.isArray(res) ? res : []);
    } catch {
      setCharacters([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert('Image must be under 5MB');
      return;
    }
    setImageFile(file);
    const reader = new FileReader();
    reader.onload = () => setImagePreview(reader.result as string);
    reader.readAsDataURL(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    if (!imageFile) {
      alert('Please upload an image for your character');
      return;
    }

    setCreating(true);
    try {
      const result = await api.createCharacter(imageFile, name.trim(), description.trim());
      setCharacters(prev => [...prev, result]);
      // Reset form
      setName('');
      setDescription('');
      setImageFile(null);
      setImagePreview(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (err: any) {
      alert(err?.response?.data?.detail || 'Failed to create character');
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (characterId: string) => {
    if (!confirm('Delete this character?')) return;
    try {
      await api.client.delete(`/characters/${characterId}`);
      setCharacters(prev => prev.filter(c => c.character_id !== characterId));
    } catch {
      alert('Failed to delete character');
    }
  };

  const getImageSrc = (character: Character) => {
    const url = character.image_url;
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return `${BACKEND_URL}${url}`;
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Story Characters</h1>
          <p className="text-gray-600 mt-1">Create characters to appear in your learning stories</p>
        </div>
        <button
          onClick={() => navigate(-1)}
          className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          ← Back
        </button>
      </div>

      {/* Create Character Form */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Create New Character</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Left: Form Fields */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Character Name *</label>
                <input
                  type="text"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  placeholder="e.g. Luna the Explorer"
                  maxLength={100}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={description}
                  onChange={e => setDescription(e.target.value)}
                  placeholder="Describe your character's personality, role, or backstory..."
                  maxLength={500}
                  rows={4}
                  className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
                <p className="text-xs text-gray-400 mt-1">{description.length}/500</p>
              </div>
            </div>

            {/* Right: Image Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Character Image *</label>
              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-primary-400 transition-colors flex items-center justify-center overflow-hidden"
                style={{ minHeight: '200px' }}
              >
                {imagePreview ? (
                  <img src={imagePreview} alt="Preview" className="max-h-64 object-contain" />
                ) : (
                  <div className="text-center p-6">
                    <div className="text-4xl mb-2">📷</div>
                    <p className="text-gray-500 font-medium">Click to upload image</p>
                    <p className="text-gray-400 text-sm mt-1">PNG, JPG, WebP up to 5MB</p>
                  </div>
                )}
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/png,image/jpeg,image/jpg,image/webp,image/gif"
                onChange={handleFileChange}
                className="hidden"
              />
              {imageFile && (
                <button
                  type="button"
                  onClick={() => {
                    setImageFile(null);
                    setImagePreview(null);
                    if (fileInputRef.current) fileInputRef.current.value = '';
                  }}
                  className="text-sm text-red-500 hover:text-red-700 mt-2"
                >
                  Remove image
                </button>
              )}
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={creating || !name.trim() || !imageFile}
              className="px-6 py-2.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {creating ? 'Creating...' : 'Create Character'}
            </button>
          </div>
        </form>
      </div>

      {/* Character Gallery */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Your Characters {characters.length > 0 && `(${characters.length})`}
        </h2>
        {loading ? (
          <div className="text-center py-12 text-gray-500">Loading characters...</div>
        ) : characters.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-5xl mb-3">🎭</div>
            <p className="text-gray-500">No characters yet. Create your first one above!</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {characters.map(character => (
              <div key={character.character_id} className="group relative rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                <div className="aspect-square bg-gray-100">
                  <img
                    src={getImageSrc(character)}
                    alt={character.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23fef3c7" width="100" height="100"/><text x="50" y="55" text-anchor="middle" fill="%23d97706" font-size="40">🎭</text></svg>';
                    }}
                  />
                </div>
                <div className="p-2">
                  <p className="font-medium text-sm text-gray-900 truncate">{character.name}</p>
                  {character.description && (
                    <p className="text-xs text-gray-500 truncate mt-0.5">{character.description}</p>
                  )}
                </div>
                <button
                  onClick={() => handleDelete(character.character_id)}
                  className="absolute top-1 right-1 w-6 h-6 bg-red-500/80 text-white rounded-full text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-600"
                  title="Delete character"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
