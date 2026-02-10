import React, { useState, useEffect } from 'react';
import api, { BACKEND_URL } from '../services/api';
import { formatChatContent } from '../utils/helpers';
import { useLanguage } from '../contexts/LanguageContext';

interface HistoricalFigure {
    id: string;
    character_name: string;
    birth_year: string;
    death_year: string;
    key_events: string;
}

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    imageUrl?: string;
    historicalContext?: string;
    emotion?: string;
    followUpSuggestions?: string[];
}

export const TimeTravelPage: React.FC = () => {
    const [step, setStep] = useState<'select' | 'interview'>('select');
    const [figures, setFigures] = useState<HistoricalFigure[]>([]);
    const [selectedFigure, setSelectedFigure] = useState<HistoricalFigure | null>(null);
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [userInput, setUserInput] = useState('');
    const [loading, setLoading] = useState(false);
    const { selectedLanguage } = useLanguage();

    useEffect(() => {
        loadFigures();
    }, []);

    const loadFigures = async () => {
        try {
            const response = await api.client.get('/features/interview/figures');
            setFigures(response.data.figures || []);
        } catch (err) {
            console.error('Failed to load figures:', err);
            // Use fallback data
            setFigures([
                { id: 'gandhi', character_name: 'Mahatma Gandhi', birth_year: '1869', death_year: '1948', key_events: 'Salt March, Quit India' },
                { id: 'einstein', character_name: 'Albert Einstein', birth_year: '1879', death_year: '1955', key_events: 'Theory of Relativity' },
                { id: 'kalam', character_name: 'APJ Abdul Kalam', birth_year: '1931', death_year: '2015', key_events: 'Missile Man of India' },
                { id: 'curie', character_name: 'Marie Curie', birth_year: '1867', death_year: '1934', key_events: 'Discovery of Radium' },
            ]);
        }
    };

    const handleStartInterview = async (figure: HistoricalFigure) => {
        setSelectedFigure(figure);
        setStep('interview');

        setLoading(true);
        try {
            const response = await api.client.post('/features/interview/chat', {
                character_name: figure.character_name,
                user_message: "Greetings! I've traveled through time to meet you. Please introduce yourself.",
                language: selectedLanguage
            });

            setMessages([{
                role: 'assistant',
                content: response.data.message || `Hello, I am ${figure.character_name}.`,
                historicalContext: response.data.historical_context,
                emotion: response.data.emotion,
                followUpSuggestions: response.data.follow_up_suggestions
            }]);
        } catch (err) {
            console.error('Failed to start interview:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSendMessage = async () => {
        if (!userInput.trim() || !selectedFigure) return;

        const message = userInput;
        setUserInput('');
        setMessages(prev => [...prev, { role: 'user', content: message }]);

        setLoading(true);
        try {
            const response = await api.client.post('/features/interview/chat', {
                character_name: selectedFigure.character_name,
                user_message: message,
                language: selectedLanguage
            });

            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message || "Let me tell you about that...",
                imageUrl: response.data.image_url,
                historicalContext: response.data.historical_context,
                emotion: response.data.emotion,
                followUpSuggestions: response.data.follow_up_suggestions
            }]);
        } catch (err) {
            console.error('Message failed:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSuggestionClick = (suggestion: string) => {
        setUserInput(suggestion);
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">⏰ Time Travel Interview</h1>
                <p className="text-gray-600">Chat with historical figures and learn history through first-person conversations!</p>
            </div>

            {step === 'select' && (
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-8">
                    <h2 className="text-xl font-bold text-gray-800 mb-6">Choose a Historical Figure to Interview</h2>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {figures.map((figure) => (
                            <button
                                key={figure.id}
                                onClick={() => handleStartInterview(figure)}
                                className="p-4 bg-white rounded-xl border-2 border-amber-200 hover:border-amber-400 hover:shadow-lg transition-all text-center"
                            >
                                <div className="text-4xl mb-2">🎭</div>
                                <h3 className="font-bold text-gray-800">{figure.character_name}</h3>
                                <p className="text-sm text-gray-500">{figure.birth_year} - {figure.death_year}</p>
                                <p className="text-xs text-amber-600 mt-2 line-clamp-2">{figure.key_events}</p>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {step === 'interview' && selectedFigure && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white p-4">
                        <h2 className="font-bold">🎭 Interview with {selectedFigure.character_name}</h2>
                        <p className="text-sm opacity-80">{selectedFigure.birth_year} - {selectedFigure.death_year}</p>
                    </div>

                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-3/4 ${msg.role === 'user'
                                    ? 'bg-amber-500 text-white p-3 rounded-lg'
                                    : 'bg-amber-50 text-gray-800 p-4 rounded-lg border border-amber-200'
                                    }`}>
                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(msg.content) }} />

                                    {msg.imageUrl && (
                                        <img src={msg.imageUrl.startsWith('data:') ? msg.imageUrl : `${BACKEND_URL}${msg.imageUrl}`} alt="Historical" className="mt-2 rounded-lg max-w-full sepia" />
                                    )}

                                    {msg.historicalContext && (
                                        <div className="mt-3 pt-3 border-t border-amber-200">
                                            <p className="text-xs text-amber-700 italic">📜 Historical Note: {msg.historicalContext}</p>
                                        </div>
                                    )}

                                    {msg.followUpSuggestions && msg.followUpSuggestions.length > 0 && (
                                        <div className="mt-3 flex flex-wrap gap-2">
                                            {msg.followUpSuggestions.map((sug, i) => (
                                                <button
                                                    key={i}
                                                    onClick={() => handleSuggestionClick(sug)}
                                                    className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded hover:bg-amber-200"
                                                >
                                                    {sug}
                                                </button>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-amber-50 p-3 rounded-lg animate-pulse">
                                    *thoughtfully considers* ...
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
                            placeholder="Ask a question..."
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={loading}
                            className="px-6 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 disabled:opacity-50"
                        >
                            Ask
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
