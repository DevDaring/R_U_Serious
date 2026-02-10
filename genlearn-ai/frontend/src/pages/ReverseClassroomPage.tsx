import React, { useState } from 'react';
import api, { BACKEND_URL } from '../services/api';
import { formatChatContent } from '../utils/helpers';

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    imageUrl?: string;
    imageCaption?: string;
    understandingLevel?: number;
}

type Persona = 'curious_beginner' | 'skeptical_questioner' | 'easily_confused' | 'quick_learner';

const PERSONAS: { id: Persona; name: string; emoji: string; description: string }[] = [
    { id: 'curious_beginner', name: 'Curious Beginner', emoji: '🌱', description: 'Eager to learn, asks basic questions' },
    { id: 'skeptical_questioner', name: 'Skeptical Questioner', emoji: '🤔', description: 'Challenges assumptions, asks for proof' },
    { id: 'easily_confused', name: 'Easily Confused', emoji: '😵', description: 'Misunderstands easily, helps find gaps' },
    { id: 'quick_learner', name: 'Quick Learner', emoji: '⚡', description: 'Grasps fast, asks advanced questions' },
];

export const ReverseClassroomPage: React.FC = () => {
    const [step, setStep] = useState<'setup' | 'teaching'>('setup');
    const [topic, setTopic] = useState('');
    const [persona, setPersona] = useState<Persona>('curious_beginner');
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [userInput, setUserInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [totalScore, setTotalScore] = useState(0);

    const handleStart = async () => {
        if (!topic.trim()) return;
        setStep('teaching');

        // Get initial AI student response
        setLoading(true);
        try {
            const response = await api.client.post('/features/reverse-classroom/chat', {
                topic,
                persona,
                user_message: `I want to teach you about: ${topic}. Are you ready to learn?`
            });

            setMessages([{
                role: 'assistant',
                content: response.data.message || "I'm ready to learn! Please teach me!",
                understandingLevel: response.data.understanding_level || 0
            }]);
            setTotalScore(response.data.teaching_score_update || 0);
        } catch (err) {
            console.error('Failed to start:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSendMessage = async () => {
        if (!userInput.trim()) return;

        const message = userInput;
        setUserInput('');
        setMessages(prev => [...prev, { role: 'user', content: message }]);

        setLoading(true);
        try {
            const response = await api.client.post('/features/reverse-classroom/chat', {
                topic,
                persona,
                user_message: message
            });

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message || "Hmm, I'm trying to understand...",
                imageUrl: response.data.image_url,
                imageCaption: response.data.image_caption,
                understandingLevel: response.data.understanding_level
            }]);
            setTotalScore(prev => prev + (response.data.teaching_score_update || 0));
        } catch (err) {
            console.error('Message failed:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🎓 Reverse Classroom</h1>
                <p className="text-gray-600">Become the teacher! Explain a topic to your AI student.</p>
            </div>

            {step === 'setup' && (
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-8">
                    <h2 className="text-xl font-bold text-gray-800 mb-6">Set Up Your Teaching Session</h2>

                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">What topic will you teach?</label>
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="e.g., Photosynthesis, Quadratic Equations, World War 2..."
                            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                    </div>

                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">Choose your student type:</label>
                        <div className="grid grid-cols-2 gap-4">
                            {PERSONAS.map((p) => (
                                <button
                                    key={p.id}
                                    onClick={() => setPersona(p.id)}
                                    className={`p-4 rounded-lg border-2 text-left transition-all ${persona === p.id
                                        ? 'border-purple-500 bg-purple-50'
                                        : 'border-gray-200 hover:border-purple-300'
                                        }`}
                                >
                                    <span className="text-2xl">{p.emoji}</span>
                                    <h3 className="font-bold text-gray-800 mt-1">{p.name}</h3>
                                    <p className="text-sm text-gray-600">{p.description}</p>
                                </button>
                            ))}
                        </div>
                    </div>

                    <button
                        onClick={handleStart}
                        disabled={!topic.trim()}
                        className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-bold hover:from-purple-600 hover:to-pink-600 disabled:opacity-50"
                    >
                        🎓 Start Teaching
                    </button>
                </div>
            )}

            {step === 'teaching' && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4 flex justify-between items-center">
                        <div>
                            <h2 className="font-bold">Teaching: {topic}</h2>
                            <p className="text-sm opacity-80">Student: {PERSONAS.find(p => p.id === persona)?.name}</p>
                        </div>
                        <div className="text-right">
                            <div className="text-2xl font-bold">⭐ {totalScore}</div>
                            <div className="text-xs opacity-80">Teaching Score</div>
                        </div>
                    </div>

                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-3/4 p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-purple-500 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                    }`}>
                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(msg.content) }} />
                                    {msg.imageUrl && (
                                        <div className="mt-2">
                                            <img src={msg.imageUrl.startsWith('data:') ? msg.imageUrl : `${BACKEND_URL}${msg.imageUrl}`} alt="Understanding" className="rounded-lg max-w-full" />
                                            {msg.imageCaption && <p className="text-sm italic mt-1">{msg.imageCaption}</p>}
                                        </div>
                                    )}
                                    {msg.understandingLevel !== undefined && msg.role === 'assistant' && (
                                        <div className="mt-2 pt-2 border-t border-gray-200">
                                            <div className="text-xs text-gray-500">Understanding: {msg.understandingLevel}%</div>
                                            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500"
                                                    style={{ width: `${msg.understandingLevel}%` }}
                                                />
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-100 p-3 rounded-lg animate-pulse">
                                    🤔 Hmm, let me think about that...
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
                            placeholder="Explain the concept to your student..."
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={loading}
                            className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:opacity-50"
                        >
                            Teach
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
