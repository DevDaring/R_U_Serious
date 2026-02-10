import React, { useState, useRef } from 'react';
import api, { BACKEND_URL } from '../services/api';
import { formatChatContent } from '../utils/helpers';

interface LearningOpportunity {
    subject: string;
    topic: string;
    hook: string;
    difficulty_level: string;
    estimated_duration: string;
    icon: string;
}

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    imageUrl?: string;
}

export const LearnFromAnythingPage: React.FC = () => {
    const [step, setStep] = useState<'upload' | 'analyzing' | 'select' | 'lesson'>('upload');
    const [opportunities, setOpportunities] = useState<LearningOpportunity[]>([]);
    const [imageDescription, setImageDescription] = useState('');
    const [selectedTopic, setSelectedTopic] = useState<LearningOpportunity | null>(null);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [userInput, setUserInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Show preview
        const reader = new FileReader();
        reader.onload = () => setImagePreview(reader.result as string);
        reader.readAsDataURL(file);

        setStep('analyzing');
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', file);

            console.log('Sending image for analysis...');
            const response = await api.client.post('/features/learn-from-image/analyze', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            console.log('Analysis response:', response.data);

            const learningOpps = response.data.learning_opportunities || [];
            setOpportunities(learningOpps);
            setImageDescription(response.data.image_description || 'Image uploaded');

            if (learningOpps.length > 0) {
                setStep('select');
            } else {
                setError('No learning opportunities found. Please try a different image.');
                setStep('upload');
            }
        } catch (err: any) {
            console.error('Image analysis failed:', err);
            setError(err?.response?.data?.detail || 'Failed to analyze image. Please try again.');
            setStep('upload');
        }
    };

    const handleTopicSelect = async (topic: LearningOpportunity) => {
        setSelectedTopic(topic);
        setStep('lesson');

        // Start the lesson
        setLoading(true);
        try {
            const response = await api.client.post('/features/learn-from-image/lesson', {
                image_description: imageDescription,
                subject: topic.subject,
                topic: topic.topic,
                grade_level: 10,
                user_message: "Start the lesson"
            });

            setMessages([{
                role: 'assistant',
                content: response.data.message || 'Let\'s begin our learning journey!',
                imageUrl: response.data.image_url
            }]);
        } catch (err) {
            console.error('Lesson start failed:', err);
            setMessages([{
                role: 'assistant',
                content: `Great! Let's learn about **${topic.topic}** from ${topic.subject}. What would you like to know first?`
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleSendMessage = async () => {
        if (!userInput.trim() || !selectedTopic) return;

        const userMessage = userInput;
        setUserInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        setLoading(true);
        try {
            const response = await api.client.post('/features/learn-from-image/lesson', {
                image_description: imageDescription,
                subject: selectedTopic.subject,
                topic: selectedTopic.topic,
                grade_level: 10,
                user_message: userMessage
            });

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message || 'I see!',
                imageUrl: response.data.image_url
            }]);
        } catch (err) {
            console.error('Message failed:', err);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "I'm having trouble responding. Please try again!"
            }]);
        } finally {
            setLoading(false);
        }
    };

    const resetToUpload = () => {
        setStep('upload');
        setOpportunities([]);
        setImagePreview(null);
        setImageDescription('');
        setSelectedTopic(null);
        setMessages([]);
        setError(null);
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">📸 Learn from Anything</h1>
                <p className="text-gray-600">Upload any image and discover multiple learning opportunities!</p>
            </div>

            {/* Upload Step */}
            {step === 'upload' && (
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8 text-center">
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                    />

                    {error && (
                        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
                            {error}
                        </div>
                    )}

                    <div className="text-6xl mb-4">📷</div>
                    <h2 className="text-xl font-bold text-gray-800 mb-4">Upload an Image</h2>
                    <p className="text-gray-600 mb-6">Take a photo or upload any image - we'll find learning opportunities in it!</p>

                    <div className="flex justify-center gap-4">
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg font-medium hover:from-blue-600 hover:to-indigo-600"
                        >
                            📁 Upload Image
                        </button>
                    </div>
                </div>
            )}

            {/* Analyzing Step */}
            {step === 'analyzing' && (
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-8">
                    {imagePreview && (
                        <div className="mb-6">
                            <img src={imagePreview} alt="Uploaded" className="max-h-48 mx-auto rounded-lg shadow-md" />
                        </div>
                    )}
                    <div className="text-center">
                        <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                        <p className="text-lg text-gray-700 font-medium">🔍 Analyzing your image...</p>
                        <p className="text-gray-500 mt-2">Finding learning opportunities across different subjects</p>
                    </div>
                </div>
            )}

            {/* Select Topic Step */}
            {step === 'select' && (
                <div className="space-y-4">
                    {imagePreview && (
                        <div className="bg-white rounded-xl p-4 shadow-lg">
                            <img src={imagePreview} alt="Uploaded" className="max-h-48 mx-auto rounded-lg" />
                            <p className="text-center text-gray-600 mt-2">{imageDescription}</p>
                        </div>
                    )}

                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <h2 className="text-xl font-bold text-gray-800 mb-4">🎓 Choose a Learning Path</h2>
                        <p className="text-gray-600 mb-4">Select a topic to start learning!</p>

                        {opportunities.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {opportunities.map((opp, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => handleTopicSelect(opp)}
                                        className="p-4 bg-gradient-to-br from-gray-50 to-white border-2 border-gray-200 rounded-xl hover:border-blue-400 hover:shadow-md transition-all text-left"
                                    >
                                        <span className="text-2xl">{opp.icon || '📚'}</span>
                                        <h3 className="font-bold text-gray-800 mt-2">{opp.subject}</h3>
                                        <p className="text-sm text-gray-600">{opp.topic}</p>
                                        <p className="text-xs text-blue-600 mt-2 italic">{opp.hook}</p>
                                        <div className="flex gap-2 mt-2 text-xs text-gray-500">
                                            <span>⏱️ {opp.estimated_duration}</span>
                                            <span>📊 {opp.difficulty_level}</span>
                                        </div>
                                    </button>
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-8">
                                <p className="text-gray-500">No learning opportunities found.</p>
                                <button onClick={resetToUpload} className="mt-4 text-blue-500 hover:underline">
                                    Try another image
                                </button>
                            </div>
                        )}
                    </div>

                    <button
                        onClick={resetToUpload}
                        className="w-full py-2 text-gray-600 hover:text-gray-800"
                    >
                        ← Upload Different Image
                    </button>
                </div>
            )}

            {/* Lesson Chat Step */}
            {step === 'lesson' && selectedTopic && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-4">
                        <div className="flex justify-between items-center">
                            <h2 className="font-bold">{selectedTopic.icon || '📚'} {selectedTopic.subject}: {selectedTopic.topic}</h2>
                            <button onClick={resetToUpload} className="text-white/80 hover:text-white text-sm">
                                ✕ Exit
                            </button>
                        </div>
                    </div>

                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                    }`}>
                                    <div
                                        className="prose prose-sm max-w-none"
                                        dangerouslySetInnerHTML={{
                                            __html: formatChatContent(msg.content)
                                        }}
                                    />
                                    {msg.imageUrl && (
                                        <img src={msg.imageUrl.startsWith('data:') ? msg.imageUrl : `${BACKEND_URL}${msg.imageUrl}`} alt="Lesson" className="mt-2 rounded-lg max-w-full" />
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-100 p-3 rounded-lg animate-pulse">
                                    Thinking...
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="p-4 border-t flex gap-2">
                        <input
                            type="text"
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                            placeholder="Ask a question or say 'continue'..."
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={loading}
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={loading || !userInput.trim()}
                            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                        >
                            Send
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
