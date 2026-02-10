import React, { useState, useEffect, useRef } from 'react';
import { Button } from '../components/common/Button';
import api, { BACKEND_URL } from '../services/api';

interface Character {
  character_id: string;
  name: string;
  description: string;
  image_url: string;
  creation_method: string;
  created_at: string;
}

const FUNNY_CHARACTER_PROMPTS = [
  { name: "Professor Brainiac", prompt: "A wise owl professor wearing graduation cap and tiny glasses, holding a book, standing at a chalkboard with equations, cartoon style, warm colors", description: "A wise owl who loves teaching science" },
  { name: "Captain Adventure", prompt: "A brave cartoon explorer fox with a compass and adventure hat, looking through binoculars, jungle background, exciting and colorful", description: "An adventurous fox who explores the world" },
  { name: "Chef Yummy", prompt: "A cheerful bear chef with a tall white hat, mixing ingredients in a big bowl, kitchen background with delicious food, warm and inviting cartoon style", description: "A friendly bear who makes learning delicious" },
  { name: "Detective Clues", prompt: "A smart mouse detective with magnifying glass and detective hat, looking for clues, mysterious but fun cartoon style, cool colors", description: "A clever mouse who solves mysteries" },
  { name: "Melody the Musician", prompt: "A happy bunny playing a colorful guitar, musical notes floating around, rainbow stage background, joyful cartoon style", description: "A musical bunny who teaches through songs" },
  { name: "Sparky the Inventor", prompt: "An energetic squirrel inventor with goggles and tool belt, surrounded by cool gadgets and gears, steampunk cartoon style, bronze and copper colors", description: "A genius squirrel who builds amazing things" },
  { name: "Flora the Nature Guide", prompt: "A gentle deer surrounded by flowers and butterflies, in a beautiful forest clearing, magical nature cartoon style, green and pink colors", description: "A kind deer who teaches about nature" },
  { name: "Zoom the Speedster", prompt: "A fast cheetah wearing racing goggles and sneakers, running with speed lines, exciting action pose, dynamic cartoon style, orange and yellow", description: "A speedy cheetah who makes learning fast and fun" },
];

// Simple Drawing Canvas Component (inline)
const SimpleDrawingCanvas: React.FC<{
  onSave?: (dataUrl: string) => void;
  canvasRef: React.RefObject<HTMLCanvasElement>;
}> = ({ canvasRef }) => {
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

  const colors = ['#000000', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#800080', '#ffc0cb', '#000000'];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-sm font-medium text-gray-700">Colors:</span>
        {colors.map((color) => (
          <button
            key={color}
            onClick={() => setBrushColor(color)}
            className={`w-8 h-8 rounded-full border-2 transition-transform ${brushColor === color ? 'border-gray-800 scale-110' : 'border-gray-300'
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

export const CharactersPage: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showGenerator, setShowGenerator] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');
  const [customName, setCustomName] = useState('');
  const [customDescription, setCustomDescription] = useState('');
  const [generatingId, setGeneratingId] = useState<string | null>(null);

  // Upload section state
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadPreview, setUploadPreview] = useState<string | null>(null);
  const [uploadName, setUploadName] = useState('');
  const [uploadDescription, setUploadDescription] = useState('');
  const [uploadPrompt, setUploadPrompt] = useState('');
  const [uploadStyle, setUploadStyle] = useState<'cartoon' | 'realistic'>('cartoon');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Drawing section state
  const [drawingName, setDrawingName] = useState('');
  const [drawingDescription, setDrawingDescription] = useState('');
  const [drawingPrompt, setDrawingPrompt] = useState('');
  const [drawingStyle, setDrawingStyle] = useState<'cartoon' | 'realistic'>('cartoon');
  const drawingCanvasRef = useRef<HTMLCanvasElement>(null!);

  useEffect(() => {
    loadCharacters();
  }, []);

  const loadCharacters = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/characters/list');
      setCharacters(response.data);
    } catch (err: any) {
      setError('Failed to load characters');
    } finally {
      setIsLoading(false);
    }
  };

  const generateFunnyCharacter = async (charData: { name: string; prompt: string; description: string }) => {
    setIsGenerating(true);
    setGeneratingId(charData.name);
    setError(null);

    try {
      const response = await api.post('/characters/generate', {
        name: charData.name,
        prompt: charData.prompt,
        description: charData.description,
        style: 'cartoon'
      });

      setCharacters(prev => [response.data, ...prev]);
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate character');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  const generateCustomCharacter = async () => {
    if (!customPrompt.trim() || !customName.trim()) return;

    setIsGenerating(true);
    setGeneratingId('custom');
    setError(null);

    try {
      const response = await api.post('/characters/generate', {
        name: customName,
        prompt: customPrompt,
        description: customDescription || `A custom character named ${customName}`,
        style: 'cartoon'
      });

      setCharacters(prev => [response.data, ...prev]);
      setCustomPrompt('');
      setCustomName('');
      setCustomDescription('');
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate character');
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
    if (!uploadedFile || !uploadName.trim() || !uploadDescription.trim()) return;

    setIsGenerating(true);
    setGeneratingId('upload');
    setError(null);

    try {
      const response = await api.createCharacterFromUpload(
        uploadedFile,
        uploadName,
        uploadDescription,
        uploadStyle,
        uploadPrompt
      );

      setCharacters(prev => [response, ...prev]);
      // Reset upload form
      setUploadedFile(null);
      setUploadPreview(null);
      setUploadName('');
      setUploadDescription('');
      setUploadPrompt('');
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate character from image');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  const generateFromDrawing = async () => {
    if (!drawingCanvasRef.current || !drawingName.trim() || !drawingDescription.trim()) return;

    setIsGenerating(true);
    setGeneratingId('drawing');
    setError(null);

    try {
      const dataUrl = drawingCanvasRef.current.toDataURL('image/png');
      const response = await api.createCharacterFromDrawing(
        dataUrl,
        drawingName,
        drawingDescription,
        drawingStyle,
        drawingPrompt
      );

      setCharacters(prev => [response, ...prev]);
      // Reset drawing form
      setDrawingName('');
      setDrawingDescription('');
      setDrawingPrompt('');
      // Clear canvas
      const ctx = drawingCanvasRef.current.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, drawingCanvasRef.current.width, drawingCanvasRef.current.height);
      }
      setShowGenerator(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate character from drawing');
    } finally {
      setIsGenerating(false);
      setGeneratingId(null);
    }
  };

  const deleteCharacter = async (characterId: string) => {
    if (!confirm('Are you sure you want to delete this character?')) return;

    try {
      await api.delete(`/characters/${characterId}`);
      setCharacters(prev => prev.filter(c => c.character_id !== characterId));
    } catch (err: any) {
      setError('Failed to delete character');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-md">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Characters</h1>
            <p className="text-gray-600 mt-1">Create fun characters that will appear in your learning stories!</p>
          </div>
          <Button onClick={() => setShowGenerator(!showGenerator)} variant="primary">
            {showGenerator ? 'Close Generator' : '🎭 Create New Character'}
          </Button>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border-2 border-red-300 rounded-lg p-4 text-red-800">
            {error}
          </div>
        )}

        {/* Character Generator Section */}
        {showGenerator && (
          <div className="mb-8 bg-gradient-to-r from-orange-50 to-yellow-50 rounded-xl p-6 border-2 border-orange-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">🎭 Create Your Character</h2>

            {/* Quick Generate - Fun Characters */}
            <div className="mb-6">
              <h3 className="font-semibold text-gray-700 mb-3">Quick Generate - Pick a Story Character:</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {FUNNY_CHARACTER_PROMPTS.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => generateFunnyCharacter(item)}
                    disabled={isGenerating}
                    className={`p-4 rounded-lg border-2 transition-all text-left ${generatingId === item.name
                      ? 'border-orange-500 bg-orange-100'
                      : 'border-gray-200 hover:border-orange-400 hover:bg-orange-50'
                      } ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    <div className="text-2xl mb-1">
                      {item.name.includes('Professor') && '🦉'}
                      {item.name.includes('Captain') && '🦊'}
                      {item.name.includes('Chef') && '🐻'}
                      {item.name.includes('Detective') && '🐭'}
                      {item.name.includes('Melody') && '🐰'}
                      {item.name.includes('Sparky') && '🐿️'}
                      {item.name.includes('Flora') && '🦌'}
                      {item.name.includes('Zoom') && '🐆'}
                    </div>
                    <div className="font-medium text-sm text-gray-800">{item.name}</div>
                    <div className="text-xs text-gray-500 mt-1 line-clamp-2">{item.description}</div>
                    {generatingId === item.name && (
                      <div className="text-xs text-orange-600 mt-1">Generating...</div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Character Generator */}
            <div className="border-t-2 border-orange-200 pt-4">
              <h3 className="font-semibold text-gray-700 mb-3">Or Create Your Own:</h3>
              <div className="space-y-3">
                <input
                  type="text"
                  value={customName}
                  onChange={(e) => setCustomName(e.target.value)}
                  placeholder="Character name (e.g., Buddy the Helper)"
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 bg-white text-gray-900"
                />
                <input
                  type="text"
                  value={customDescription}
                  onChange={(e) => setCustomDescription(e.target.value)}
                  placeholder="Short description (e.g., A friendly robot who helps with math)"
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 bg-white text-gray-900"
                />
                <textarea
                  value={customPrompt}
                  onChange={(e) => setCustomPrompt(e.target.value)}
                  placeholder="Describe how your character looks (e.g., A happy blue robot with big friendly eyes, antennas on head, waving hand)"
                  className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-200 bg-white text-gray-900 resize-none h-24"
                />
                <Button
                  onClick={generateCustomCharacter}
                  disabled={isGenerating || !customPrompt.trim() || !customName.trim()}
                  isLoading={generatingId === 'custom'}
                  variant="primary"
                >
                  🎭 Generate Custom Character
                </Button>
              </div>
            </div>

            {/* Upload Image Section */}
            <div className="border-t-2 border-orange-200 pt-6 mt-6">
              <h3 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-xl">📷</span> Upload an Image to Create Character:
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Upload any image and AI will transform it into a full-body story character with a fun background!
              </p>

              <div className="grid md:grid-cols-2 gap-6">
                {/* Upload Area */}
                <div>
                  {!uploadPreview ? (
                    <div
                      onDragOver={(e) => e.preventDefault()}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      className="border-3 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:border-orange-400 hover:bg-orange-25 transition-colors"
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
                    placeholder="Character name *"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-orange-500 bg-white text-gray-900"
                  />
                  <input
                    type="text"
                    value={uploadDescription}
                    onChange={(e) => setUploadDescription(e.target.value)}
                    placeholder="Character description/role *"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-orange-500 bg-white text-gray-900"
                  />
                  <textarea
                    value={uploadPrompt}
                    onChange={(e) => setUploadPrompt(e.target.value)}
                    placeholder="Optional: Add instructions (e.g., 'Make it a superhero', 'Add a wizard cape')"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-orange-500 bg-white text-gray-900 resize-none h-20"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => setUploadStyle('cartoon')}
                      className={`flex-1 py-2 rounded-lg font-medium ${uploadStyle === 'cartoon' ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-700'
                        }`}
                    >
                      🎨 Cartoon
                    </button>
                    <button
                      onClick={() => setUploadStyle('realistic')}
                      className={`flex-1 py-2 rounded-lg font-medium ${uploadStyle === 'realistic' ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-700'
                        }`}
                    >
                      📸 Realistic
                    </button>
                  </div>
                  <Button
                    onClick={generateFromUpload}
                    disabled={isGenerating || !uploadedFile || !uploadName.trim() || !uploadDescription.trim()}
                    isLoading={generatingId === 'upload'}
                    variant="primary"
                    className="w-full"
                  >
                    ✨ Generate Character from Image
                  </Button>
                </div>
              </div>
            </div>

            {/* Drawing Section */}
            <div className="border-t-2 border-orange-200 pt-6 mt-6">
              <h3 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="text-xl">🎨</span> Draw Your Own Character:
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Draw anything and AI will transform it into a polished full-body story character with a scene!
              </p>

              <div className="grid md:grid-cols-2 gap-6">
                {/* Canvas */}
                <div>
                  <SimpleDrawingCanvas onSave={() => { }} canvasRef={drawingCanvasRef} />
                </div>

                {/* Drawing Options */}
                <div className="space-y-3">
                  <input
                    type="text"
                    value={drawingName}
                    onChange={(e) => setDrawingName(e.target.value)}
                    placeholder="Character name *"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-orange-500 bg-white text-gray-900"
                  />
                  <input
                    type="text"
                    value={drawingDescription}
                    onChange={(e) => setDrawingDescription(e.target.value)}
                    placeholder="Character description/role *"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-orange-500 bg-white text-gray-900"
                  />
                  <textarea
                    value={drawingPrompt}
                    onChange={(e) => setDrawingPrompt(e.target.value)}
                    placeholder="Optional: Add instructions (e.g., 'Make it a cute robot', 'Add space theme')"
                    className="w-full px-4 py-2 rounded-lg border-2 border-gray-300 focus:border-orange-500 bg-white text-gray-900 resize-none h-20"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => setDrawingStyle('cartoon')}
                      className={`flex-1 py-2 rounded-lg font-medium ${drawingStyle === 'cartoon' ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-700'
                        }`}
                    >
                      🎨 Cartoon
                    </button>
                    <button
                      onClick={() => setDrawingStyle('realistic')}
                      className={`flex-1 py-2 rounded-lg font-medium ${drawingStyle === 'realistic' ? 'bg-orange-600 text-white' : 'bg-gray-200 text-gray-700'
                        }`}
                    >
                      📸 Realistic
                    </button>
                  </div>
                  <Button
                    onClick={generateFromDrawing}
                    disabled={isGenerating || !drawingName.trim() || !drawingDescription.trim()}
                    isLoading={generatingId === 'drawing'}
                    variant="primary"
                    className="w-full"
                  >
                    ✨ Generate Character from Drawing
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Character Gallery */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-gray-600">Loading your characters...</p>
          </div>
        ) : characters.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-xl">
            <div className="text-6xl mb-4">🎭</div>
            <p className="text-gray-600 text-lg">No characters yet!</p>
            <p className="text-gray-500 mt-2">Click "Create New Character" to generate fun story companions</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {characters.map((character) => (
              <div
                key={character.character_id}
                className="relative rounded-xl overflow-hidden border-2 border-gray-200 hover:border-orange-300 transition-all hover:shadow-lg"
              >
                <img
                  src={`${BACKEND_URL}${character.image_url}`}
                  alt={character.name}
                  className="w-full aspect-[3/4] object-cover"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23fef3c7" width="100" height="100"/><text x="50" y="55" text-anchor="middle" fill="%23d97706" font-size="40">🎭</text></svg>';
                  }}
                />
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3">
                  <p className="text-white font-bold truncate">{character.name}</p>
                  <p className="text-gray-300 text-xs truncate">{character.description}</p>
                  <div className="flex gap-2 mt-2">
                    <button
                      onClick={() => deleteCharacter(character.character_id)}
                      className="text-xs bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                    >
                      🗑️ Delete
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
