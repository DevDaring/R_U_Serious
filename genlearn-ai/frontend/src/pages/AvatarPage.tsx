import React, { useState, useEffect, useRef } from 'react';
import { Button } from '../components/common/Button';
import api, { BACKEND_URL } from '../services/api';
import { useAuth } from '../hooks/useAuth';

interface Avatar {
  avatar_id: string;
  name: string;
  image_url: string;
  style: string;
  creation_method: string;
  created_at: string;
}

const FUNNY_AVATAR_PROMPTS = [
  { name: "Goofy Scientist", prompt: "A funny cartoon scientist with wild Einstein-like hair, oversized glasses, and a surprised expression, wearing a lab coat with colorful stains, bright and cheerful" },
  { name: "Cool Space Cat", prompt: "A cute cartoon cat wearing a space helmet and astronaut suit, floating in space with stars around, looking confident and cool, vibrant colors" },
  { name: "Ninja Penguin", prompt: "An adorable penguin dressed as a ninja with a black headband, holding tiny throwing stars, looking determined but cute, cartoon style" },
  { name: "Wizard Panda", prompt: "A chubby cute panda wearing a purple wizard hat with stars, holding a magical wand with sparkles, cartoon style, friendly expression" },
  { name: "Robot Chef", prompt: "A friendly cartoon robot wearing a chef hat and apron, holding a frying pan with delicious food, with steam rising, cheerful metallic design" },
  { name: "Superhero Dog", prompt: "A heroic golden retriever dog wearing a red cape and mask, flying pose with one paw forward, determined expression, cartoon superhero style" },
  { name: "Pirate Parrot", prompt: "A colorful cartoon parrot wearing a tiny pirate hat and eyepatch, perched on treasure chest, saying 'Arrr!', tropical colors" },
  { name: "Dancing Dinosaur", prompt: "A cute T-Rex dinosaur doing a funny dance move, wearing headphones, colorful disco background, happy expression, cartoon style" },
];

// Simple Drawing Canvas Component (inline)
const SimpleDrawingCanvas: React.FC<{
  onSave: (dataUrl: string) => void;
  canvasRef: React.RefObject<HTMLCanvasElement | null>;
}> = ({ onSave, canvasRef }) => {
  const [isDrawing, setIsDrawing] = useState(false);
  const [brushColor, setBrushColor] = useState('#000000');
  const [brushSize, setBrushSize] = useState(5);
  const contextRef = useRef<CanvasRenderingContext2D | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    canvas.width = 400;
    canvas.height = 400;
    
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.lineCap = 'round';
      ctx.strokeStyle = brushColor;
      ctx.lineWidth = brushSize;
      contextRef.current = ctx;
    }
  }, []);

  useEffect(() => {
    if (contextRef.current) {
      contextRef.current.strokeStyle = brushColor;
      contextRef.current.lineWidth = brushSize;
    }
  }, [brushColor, brushSize]);

  const startDrawing = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas || !contextRef.current) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    contextRef.current.beginPath();
    contextRef.current.moveTo(x, y);
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || !contextRef.current || !canvasRef.current) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    contextRef.current.lineTo(x, y);
    contextRef.current.stroke();
  };

  const stopDrawing = () => {
    if (contextRef.current) {
      contextRef.current.closePath();
    }
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas || !contextRef.current) return;
    
    contextRef.current.fillStyle = '#ffffff';
    contextRef.current.fillRect(0, 0, canvas.width, canvas.height);
  };

  const colors = ['#000000', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#800080', '#ffc0cb'];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-sm font-medium text-gray-700">Colors:</span>
        {colors.map((color) => (
          <button
            key={color}
            onClick={() => setBrushColor(color)}
            className={`w-8 h-8 rounded-full border-2 transition-transform ${
              brushColor === color ? 'border-gray-800 scale-110' : 'border-gray-300'
            }`}
            style={{ backgroundColor: color }}
          />
        ))}
        <input
          type="color"
          value={brushColor}
          onChange={(e) => setBrushColor(e.target.value)}
          className="w-8 h-8 rounded cursor-pointer"
        />
      </div>
      
      <div className="flex items-center gap-4">
        <span className="text-sm font-medium text-gray-700">Brush: {brushSize}px</span>
        <input
          type="range"
          min="1"
          max="30"
          value={brushSize}
          onChange={(e) => setBrushSize(Number(e.target.value))}
          className="flex-1 max-w-[200px]"
        />
        <button
          onClick={clearCanvas}
          className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
        >
          Clear
        </button>
      </div>
      
      <div className="border-2 border-gray-300 rounded-lg overflow-hidden inline-block bg-white">
        <canvas
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          className="cursor-crosshair"
        />
      </div>
    </div>
  );
};

export const AvatarPage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [avatars, setAvatars] = useState<Avatar[]>([]);
  const [selectedAvatar, setSelectedAvatar] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showGenerator, setShowGenerator] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');
  const [customName, setCustomName] = useState('');
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  
  // Upload section state
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadPreview, setUploadPreview] = useState<string | null>(null);
  const [uploadName, setUploadName] = useState('');
  const [uploadPrompt, setUploadPrompt] = useState('');
  const [uploadStyle, setUploadStyle] = useState<'cartoon' | 'realistic'>('cartoon');
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Drawing section state
  const [drawingName, setDrawingName] = useState('');
  const [drawingPrompt, setDrawingPrompt] = useState('');
  const [drawingStyle, setDrawingStyle] = useState<'cartoon' | 'realistic'>('cartoon');
  const drawingCanvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    loadAvatars();
  }, []);

  const loadAvatars = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/avatar/list');
      setAvatars(response.data);
      if (user?.avatar_id) {
        setSelectedAvatar(user.avatar_id);
      }
    } catch (err: any) {
      setError('Failed to load avatars');
    } finally {
      setIsLoading(false);
    }
  };

  const generateFunnyAvatar = async (promptData: { name: string; prompt: string }) => {
    setIsGenerating(true);
    setGeneratingId(promptData.name);
    setError(null);
    
    try {
      const response = await api.post('/avatar/generate', {
        name: promptData.name,
        prompt: promptData.prompt,
        style: 'cartoon'
      });
      
      setAvatars(prev => [response.data, ...prev]);
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate avatar');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  const generateCustomAvatar = async () => {
    if (!customPrompt.trim() || !customName.trim()) return;
    
    setIsGenerating(true);
    setGeneratingId('custom');
    setError(null);
    
    try {
      const response = await api.post('/avatar/generate', {
        name: customName,
        prompt: customPrompt,
        style: 'cartoon'
      });
      
      setAvatars(prev => [response.data, ...prev]);
      setCustomPrompt('');
      setCustomName('');
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate avatar');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  // Handle file upload
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
      setError('Image must be less than 5MB');
      return;
    }
    
    setUploadedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => setUploadPreview(e.target?.result as string);
    reader.readAsDataURL(file);
    setError(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
      setError('Please drop an image file');
      return;
    }
    
    setUploadedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => setUploadPreview(e.target?.result as string);
    reader.readAsDataURL(file);
    setError(null);
  };

  const generateFromUpload = async () => {
    if (!uploadedFile || !uploadName.trim()) return;
    
    setIsGenerating(true);
    setGeneratingId('upload');
    setError(null);
    
    try {
      const response = await api.createAvatarFromUpload(
        uploadedFile,
        uploadName,
        uploadStyle,
        uploadPrompt
      );
      
      setAvatars(prev => [response, ...prev]);
      // Reset upload form
      setUploadedFile(null);
      setUploadPreview(null);
      setUploadName('');
      setUploadPrompt('');
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate avatar from image');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  const generateFromDrawing = async () => {
    if (!drawingCanvasRef.current || !drawingName.trim()) return;
    
    setIsGenerating(true);
    setGeneratingId('drawing');
    setError(null);
    
    try {
      const dataUrl = drawingCanvasRef.current.toDataURL('image/png');
      const response = await api.createAvatarFromDrawing(
        dataUrl,
        drawingName,
        drawingStyle,
        drawingPrompt
      );
      
      setAvatars(prev => [response, ...prev]);
      // Reset drawing form
      setDrawingName('');
      setDrawingPrompt('');
      // Clear canvas
      const ctx = drawingCanvasRef.current.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, drawingCanvasRef.current.width, drawingCanvasRef.current.height);
      }
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate avatar from drawing');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  const setAsActiveAvatar = async (avatarId: string) => {
    try {
      await api.post('/avatar/set-active', { avatar_id: avatarId });
      setSelectedAvatar(avatarId);
      if (updateUser) {
        updateUser({ ...user!, avatar_id: avatarId });
      }
    } catch (err: any) {
      setError('Failed to set avatar');
    }
  };

  const deleteAvatar = async (avatarId: string) => {
    if (!confirm('Are you sure you want to delete this avatar?')) return;
    
    try {
      await api.delete(`/avatar/${avatarId}`);
      setAvatars(prev => prev.filter(a => a.avatar_id !== avatarId));
      if (selectedAvatar === avatarId) {
        setSelectedAvatar(null);
      }
    } catch (err: any) {
      setError('Failed to delete avatar');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-md">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Avatars</h1>
            <p className="text-gray-600 mt-1">Create fun avatars using AI to personalize your learning journey</p>
          </div>
          <Button onClick={() => setShowGenerator(!showGenerator)} variant="primary">
            {showGenerator ? 'Close Generator' : '✨ Create New Avatar'}
          </Button>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border-2 border-red-300 rounded-lg p-4 text-red-800">
            {error}
          </div>
        )}

        {/* Avatar Generator Section */}
        {showGenerator && (
          <div className="mb-8 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 border-2 border-purple-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">🎨 Create Your Avatar</h2>
            
            {/* Quick Generate - Funny Avatars */}
            <div className="mb-6">
              <h3 className="font-semibold text-gray-700 mb-3">Quick Generate - Pick a Fun Character:</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {FUNNY_AVATAR_PROMPTS.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => generateFunnyAvatar(item)}
                    disabled={isGenerating}
                    className={`p-4 rounded-lg border-2 transition-all text-left ${
                      generatingId === item.name 
                        ? 'border-purple-500 bg-purple-100' 
                        : 'border-gray-200 hover:border-purple-400 hover:bg-purple-50'
                    } ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    <div className="text-2xl mb-1">
                      {item.name.includes('Scientist') && '🔬'}
                      {item.name.includes('Cat') && '🐱'}
                      {item.name.includes('Penguin') && '🐧'}
                      {item.name.includes('Panda') && '🐼'}
                      {item.name.includes('Robot') && '🤖'}
                      {item.name.includes('Dog') && '🐕'}
                      {item.name.includes('Parrot') && '🦜'}
                      {item.name.includes('Dinosaur') && '🦖'}
                    </div>
                    <div className="font-medium text-sm text-gray-800">{item.name}</div>
                    {generatingId === item.name && (
                      <div className="text-xs text-purple-600 mt-1">Generating...</div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Avatar Generator */}
            <div className="border-t-2 border-purple-200 pt-4">
              <h3 className="font-semibold text-gray-700 mb-3">Or Create Your Own:</h3>
              <div className="space-y-3">
                <input
                  type="text"
                  value={customName}
                  onChange={(e) => setCustomName(e.target.value)}
                  placeholder="Avatar name (e.g., My Cool Hero)"
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-purple-500 focus:ring-2 focus:ring-purple-200 bg-white text-gray-900"
                />
                <textarea
                  value={customPrompt}
                  onChange={(e) => setCustomPrompt(e.target.value)}
                  placeholder="Describe your avatar (e.g., A magical unicorn with rainbow mane, wearing sunglasses, looking super cool)"
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-purple-500 focus:ring-2 focus:ring-purple-200 bg-white text-gray-900 resize-none h-24"
                />
                <Button
                  onClick={generateCustomAvatar}
                  disabled={isGenerating || !customPrompt.trim() || !customName.trim()}
                  isLoading={generatingId === 'custom'}
                  variant="primary"
                >
                  ✨ Generate Custom Avatar
                </Button>
              </div>
            </div>

            {/* Upload Image Section */}
            <div className="border-t-2 border-purple-200 pt-6 mt-6">
              <h3 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-xl">📷</span> Upload an Image to Create Avatar:
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Upload any image and AI will transform it into a unique avatar. Optionally add instructions to customize the result.
              </p>
              
              <div className="grid md:grid-cols-2 gap-6">
                {/* Upload Area */}
                <div>
                  {!uploadPreview ? (
                    <div
                      onDragOver={(e) => e.preventDefault()}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      className="border-3 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-purple-400 hover:bg-purple-25 transition-colors"
                    >
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        onChange={handleFileSelect}
                        className="hidden"
                      />
                      <div className="text-4xl mb-2">📤</div>
                      <p className="text-gray-700 font-medium">Click or drag & drop image</p>
                      <p className="text-sm text-gray-500 mt-1">JPG, PNG, GIF (max 5MB)</p>
                    </div>
                  ) : (
                    <div className="relative">
                      <img
                        src={uploadPreview}
                        alt="Preview"
                        className="w-full h-64 object-contain rounded-xl border-2 border-gray-200 bg-gray-100"
                      />
                      <button
                        onClick={() => { setUploadedFile(null); setUploadPreview(null); }}
                        className="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full hover:bg-red-600"
                      >
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  )}
                </div>
                
                {/* Upload Options */}
                <div className="space-y-3">
                  <input
                    type="text"
                    value={uploadName}
                    onChange={(e) => setUploadName(e.target.value)}
                    placeholder="Avatar name *"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-purple-500 bg-white text-gray-900"
                  />
                  <textarea
                    value={uploadPrompt}
                    onChange={(e) => setUploadPrompt(e.target.value)}
                    placeholder="Optional: Add instructions (e.g., 'Make it look like a superhero', 'Add a wizard hat')"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-purple-500 bg-white text-gray-900 resize-none h-20"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => setUploadStyle('cartoon')}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                        uploadStyle === 'cartoon' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700'
                      }`}
                    >
                      🎨 Cartoon
                    </button>
                    <button
                      onClick={() => setUploadStyle('realistic')}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                        uploadStyle === 'realistic' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700'
                      }`}
                    >
                      📸 Realistic
                    </button>
                  </div>
                  <Button
                    onClick={generateFromUpload}
                    disabled={isGenerating || !uploadedFile || !uploadName.trim()}
                    isLoading={generatingId === 'upload'}
                    variant="primary"
                    className="w-full text-sm py-2"
                  >
                    ✨ Generate from Image
                  </Button>
                </div>
              </div>
            </div>

            {/* Drawing Section */}
            <div className="border-t-2 border-purple-200 pt-6 mt-6">
              <h3 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-xl">🎨</span> Draw Your Own Avatar:
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Draw anything and AI will transform it into a polished avatar! Optionally add instructions.
              </p>
              
              <div className="grid md:grid-cols-2 gap-6">
                {/* Canvas */}
                <div>
                  <SimpleDrawingCanvas onSave={() => {}} canvasRef={drawingCanvasRef} />
                </div>
                
                {/* Drawing Options */}
                <div className="space-y-3">
                  <input
                    type="text"
                    value={drawingName}
                    onChange={(e) => setDrawingName(e.target.value)}
                    placeholder="Avatar name *"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-purple-500 bg-white text-gray-900"
                  />
                  <textarea
                    value={drawingPrompt}
                    onChange={(e) => setDrawingPrompt(e.target.value)}
                    placeholder="Optional: Add instructions (e.g., 'Make it a cute robot', 'Turn into anime style')"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-purple-500 bg-white text-gray-900 resize-none h-20"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => setDrawingStyle('cartoon')}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                        drawingStyle === 'cartoon' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700'
                      }`}
                    >
                      🎨 Cartoon
                    </button>
                    <button
                      onClick={() => setDrawingStyle('realistic')}
                      className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
                        drawingStyle === 'realistic' ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700'
                      }`}
                    >
                      📸 Realistic
                    </button>
                  </div>
                  <Button
                    onClick={generateFromDrawing}
                    disabled={isGenerating || !drawingName.trim()}
                    isLoading={generatingId === 'drawing'}
                    variant="primary"
                    className="w-full text-sm py-2"
                  >
                    ✨ Generate from Drawing
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Avatar Gallery */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-gray-600">Loading your avatars...</p>
          </div>
        ) : avatars.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-xl">
            <div className="text-6xl mb-4">🎭</div>
            <p className="text-gray-600 text-lg">No avatars yet!</p>
            <p className="text-gray-500 mt-2">Click "Create New Avatar" to generate your first fun avatar</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {avatars.map((avatar) => (
              <div
                key={avatar.avatar_id}
                className={`relative rounded-xl overflow-hidden border-4 transition-all ${
                  selectedAvatar === avatar.avatar_id
                    ? 'border-green-500 shadow-lg shadow-green-200'
                    : 'border-gray-200 hover:border-primary-300'
                }`}
              >
                <img
                  src={`${BACKEND_URL}${avatar.image_url}`}
                  alt={avatar.name}
                  className="w-full aspect-square object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23ddd" width="100" height="100"/><text x="50" y="55" text-anchor="middle" fill="%23999" font-size="40">👤</text></svg>';
                  }}
                />
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3">
                  <p className="text-white font-medium truncate">{avatar.name}</p>
                  <div className="flex gap-2 mt-2">
                    {selectedAvatar !== avatar.avatar_id && (
                      <button
                        onClick={() => setAsActiveAvatar(avatar.avatar_id)}
                        className="flex-1 text-xs bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded"
                      >
                        Use This
                      </button>
                    )}
                    {selectedAvatar === avatar.avatar_id && (
                      <span className="flex-1 text-xs bg-green-600 text-white px-2 py-1 rounded text-center">
                        ✓ Active
                      </span>
                    )}
                    <button
                      onClick={() => deleteAvatar(avatar.avatar_id)}
                      className="text-xs bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
