import React, { useState, useEffect, useRef } from 'react';
import api, { BACKEND_URL } from '../services/api';
import { formatChatContent } from '../utils/helpers';

// Types
interface Session {
    session_id: string;
    topic: string;
    subject: string;
    current_layer: number;
    clarity_score: number;
    teaching_xp_earned: number;
}

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
    avatar_state?: string;
    confusion_level?: number;
    curiosity_level?: number;
}

interface RittyResponse {
    response: string;
    confusion_level: number;
    curiosity_level: number;
    follow_up_question?: string;
    gap_detected?: string;
    emoji_reaction: string;
    avatar_state: string;
    layer_complete: boolean;
}

interface CompressionEvaluation {
    score: number;
    word_count: number;
    within_limit: boolean;
    feedback: string;
    preserved_concepts: string[];
    lost_concepts: string[];
    suggestion?: string;
    passed: boolean;
    next_word_limit?: number;
}

interface WhySpiralResponse {
    next_question?: string;
    current_depth: number;
    boundary_detected: boolean;
    boundary_topic?: string;
    exploration_offer?: string;
    can_continue: boolean;
}

interface AnalogyEvaluation {
    phase: string;
    score: number;
    strengths: string[];
    weaknesses: string[];
    stress_test_question?: string;
    passed_stress_test?: boolean;
    save_worthy: boolean;
    analogy_image_url?: string;
}

interface PersonaFeedback {
    persona: string;
    persona_name: string;
    satisfaction: number;
    response: string;
    follow_up_question?: string;
    is_satisfied: boolean;
}

interface LectureHallResponse {
    personas: PersonaFeedback[];
    overall_satisfaction: number;
    all_satisfied: boolean;
    dominant_issue?: string;
    suggestion?: string;
}

// Ritty Avatar Component
const RittyAvatar: React.FC<{ state: string; confusion: number; curiosity: number }> = ({ state, confusion, curiosity }) => {
    const getEmoji = () => {
        switch (state) {
            case 'confused': return '😕';
            case 'curious': return '🤔';
            case 'happy': return '😊';
            case 'surprised': return '😲';
            case 'thinking': return '🧐';
            default: return '👦';
        }
    };

    return (
        <div className="flex flex-col items-center">
            <div className="text-6xl mb-2 animate-bounce">{getEmoji()}</div>
            <div className="text-sm font-bold text-amber-600">Ritty</div>
            <div className="w-full mt-2 space-y-1">
                <div className="flex items-center gap-2 text-xs">
                    <span>😕</span>
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-red-400 transition-all duration-500"
                            style={{ width: `${confusion * 100}%` }}
                        />
                    </div>
                </div>
                <div className="flex items-center gap-2 text-xs">
                    <span>✨</span>
                    <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-green-400 transition-all duration-500"
                            style={{ width: `${curiosity * 100}%` }}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export const FeynmanEnginePage: React.FC = () => {
    // State
    const [step, setStep] = useState<'setup' | 'learning'>('setup');
    const [session, setSession] = useState<Session | null>(null);
    const [currentLayer, setCurrentLayer] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Setup state
    const [topic, setTopic] = useState('');
    const [subject, setSubject] = useState('General');
    const [difficulty, setDifficulty] = useState(5);
    const [startingLayer, setStartingLayer] = useState(1);

    // Layer 1: Ritty state
    const [rittyMessages, setRittyMessages] = useState<ChatMessage[]>([]);
    const [rittyInput, setRittyInput] = useState('');
    const [avatarState, setAvatarState] = useState('neutral');
    const [confusionLevel, setConfusionLevel] = useState(0.5);
    const [curiosityLevel, setCuriosityLevel] = useState(0.5);

    // Layer 2: Compression state
    const [currentWordLimit, setCurrentWordLimit] = useState(100);
    const [compressionInput, setCompressionInput] = useState('');
    const [compressionHistory, setCompressionHistory] = useState<{ limit: number; text: string; score: number; feedback: string; suggestion?: string }[]>([]);

    // Layer 3: Why Spiral state
    const [whySpiralMessages, setWhySpiralMessages] = useState<ChatMessage[]>([]);
    const [whySpiralInput, setWhySpiralInput] = useState('');
    const [whyDepth, setWhyDepth] = useState(1);
    const [boundaryFound, setBoundaryFound] = useState(false);

    // Layer 4: Analogy state
    const [analogyPhase, setAnalogyPhase] = useState<'create' | 'defend' | 'refine'>('create');
    const [analogyInput, setAnalogyInput] = useState('');
    const [analogyFeedback, setAnalogyFeedback] = useState<AnalogyEvaluation | null>(null);
    const [stressTestQuestion, setStressTestQuestion] = useState<string | null>(null);
    const [analogyHistory, setAnalogyHistory] = useState<{ role: string; content: string; image_url?: string }[]>([]);

    // Layer 5: Lecture Hall state
    const [lectureMessages, setLectureMessages] = useState<ChatMessage[]>([]);
    const [lectureInput, setLectureInput] = useState('');
    const [personaFeedback, setPersonaFeedback] = useState<PersonaFeedback[]>([]);

    // Session History state - SAFE: Click-to-load, no useEffect
    const [showHistory, setShowHistory] = useState(false);
    const [sessionHistory, setSessionHistory] = useState<any[]>([]);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [historyError, setHistoryError] = useState<string | null>(null);

    const chatEndRef = useRef<HTMLDivElement>(null);

    // Toggle history section - loads data on first open
    const toggleHistory = () => {
        if (!showHistory && sessionHistory.length === 0 && !historyLoading) {
            loadSessionHistory();
        }
        setShowHistory(!showHistory);
    };

    // Load session history - ONLY called when user clicks
    const loadSessionHistory = async () => {
        setHistoryLoading(true);
        setHistoryError(null);
        try {
            const response = await api.client.get('/feynman/sessions/user/guest?limit=10');
            setSessionHistory(response.data.sessions || []);
        } catch (err) {
            console.error('Failed to load session history:', err);
            setHistoryError('Failed to load sessions. Click to retry.');
        } finally {
            setHistoryLoading(false);
        }
    };

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [rittyMessages, whySpiralMessages, lectureMessages]);

    // Resume a session from history
    const resumeSession = async (savedSession: any) => {
        setLoading(true);
        setError(null);
        try {
            // Set session data
            const sessionData = {
                session_id: savedSession.id,
                user_id: savedSession.user_id || 'guest',
                topic: savedSession.topic,
                subject: savedSession.subject,
                difficulty_level: savedSession.difficulty_level,
                current_layer: savedSession.current_layer || 1,
                status: savedSession.status,
                clarity_score: savedSession.clarity_score || 0,
                teaching_xp_earned: savedSession.teaching_xp_earned || 0,
                started_at: savedSession.started_at,
                completed_at: savedSession.completed_at
            };

            setSession(sessionData);
            setCurrentLayer(sessionData.current_layer);
            setStep('learning');

            // Start the layer to load history
            await startLayer(sessionData.current_layer, sessionData.session_id);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to resume session');
        } finally {
            setLoading(false);
        }
    };

    const subjects = [
        'General', 'Physics', 'Chemistry', 'Biology', 'Mathematics',
        'Computer Science', 'History', 'Geography', 'Economics', 'Psychology'
    ];

    const layerNames = [
        { id: 1, name: 'Curious Child', emoji: '👦', color: 'from-amber-500 to-orange-500' },
        { id: 2, name: 'Compression', emoji: '📝', color: 'from-blue-500 to-cyan-500' },
        { id: 3, name: 'Why Spiral', emoji: '🌀', color: 'from-purple-500 to-pink-500' },
        { id: 4, name: 'Analogy Architect', emoji: '🎨', color: 'from-green-500 to-emerald-500' },
        { id: 5, name: 'Lecture Hall', emoji: '🎓', color: 'from-red-500 to-rose-500' }
    ];

    // Start Session
    const handleStartSession = async () => {
        if (!topic.trim()) {
            setError('Please enter a topic');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await api.client.post('/feynman/session/start', {
                user_id: 'guest',
                topic: topic.trim(),
                subject,
                difficulty_level: difficulty,
                starting_layer: startingLayer
            });

            setSession(response.data);
            setCurrentLayer(startingLayer);
            setStep('learning');

            // Start the chosen layer
            await startLayer(startingLayer, response.data.session_id);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to start session');
        } finally {
            setLoading(false);
        }
    };

    // Start a specific layer
    const startLayer = async (layer: number, sessionId: string) => {
        setLoading(true);
        try {
            const response = await api.client.post(`/feynman/layer${layer}/start?session_id=${sessionId}`);
            const data = response.data;

            if (layer === 1) {
                // Handle both new session and existing history
                if (data.history && data.history.length > 0) {
                    const messages = data.history.map((h: any) => ({
                        role: h.role,
                        content: h.message,
                        avatar_state: h.role === 'assistant' ? 'curious' : undefined,
                        confusion_level: h.confusion_level,
                        curiosity_level: h.curiosity_level
                    }));
                    setRittyMessages(messages);
                    // Get last assistant message's metrics
                    const lastAssistant = data.history.filter((h: any) => h.role === 'assistant').pop();
                    if (lastAssistant) {
                        setConfusionLevel(parseFloat(lastAssistant.confusion_level) || 0.5);
                        setCuriosityLevel(parseFloat(lastAssistant.curiosity_level) || 0.5);
                    }
                } else if (data.message) {
                    setRittyMessages([{ role: 'assistant', content: data.message, avatar_state: 'curious' }]);
                    setConfusionLevel(0.5);
                    setCuriosityLevel(0.5);
                }
                setAvatarState('curious');
            } else if (layer === 2) {
                setCurrentWordLimit(data.current_word_limit || 100);
                // History for compression is handled separately via compressionHistory state
            } else if (layer === 3) {
                // Handle existing history for Why Spiral
                if (data.history && data.history.length > 0) {
                    const messages = data.history.map((h: any) => ({
                        role: h.role,
                        content: h.message
                    }));
                    setWhySpiralMessages(messages);
                    setWhyDepth(data.current_depth || 1);
                } else {
                    setWhySpiralMessages([{ role: 'assistant', content: data.question }]);
                    setWhyDepth(1);
                }
                setBoundaryFound(false);
            } else if (layer === 4) {
                // Handle existing history for Analogy
                setAnalogyPhase(data.phase || 'create');
                setAnalogyFeedback(null);
                setAnalogyInput('');
                setStressTestQuestion(null);
                // Load history with images
                if (data.history && data.history.length > 0) {
                    const historyItems = data.history.map((h: any) => ({
                        role: h.role,
                        content: h.message,
                        image_url: h.image_url || undefined
                    }));
                    setAnalogyHistory(historyItems);
                } else {
                    setAnalogyHistory([]);
                }
            } else if (layer === 5) {
                // Handle existing history for Lecture Hall
                if (data.history && data.history.length > 0) {
                    const messages = data.history.map((h: any) => ({
                        role: h.role,
                        content: h.message
                    }));
                    setLectureMessages(messages);
                } else {
                    setLectureMessages([{ role: 'assistant', content: data.message }]);
                }
                setPersonaFeedback([]);
            }
        } catch (err) {
            console.error('Failed to start layer:', err);
        } finally {
            setLoading(false);
        }
    };

    // Change layer
    const handleChangeLayer = async (newLayer: number) => {
        if (!session) return;

        setLoading(true);
        try {
            await api.client.post('/feynman/session/change-layer', {
                session_id: session.session_id,
                target_layer: newLayer
            });
            setCurrentLayer(newLayer);
            await startLayer(newLayer, session.session_id);
        } catch (err) {
            console.error('Failed to change layer:', err);
        } finally {
            setLoading(false);
        }
    };

    // Layer 1: Send message to Ritty
    const handleRittySend = async () => {
        if (!session || !rittyInput.trim()) return;

        const userMessage = rittyInput;
        setRittyInput('');
        setRittyMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        setLoading(true);
        try {
            const response = await api.client.post<RittyResponse>('/feynman/layer1/teach', {
                session_id: session.session_id,
                message: userMessage,
                layer: 1
            });

            const data = response.data;
            setRittyMessages(prev => [...prev, {
                role: 'assistant',
                content: `${data.emoji_reaction} ${data.response}${data.follow_up_question ? '\n\n' + data.follow_up_question : ''}`,
                avatar_state: data.avatar_state,
                confusion_level: data.confusion_level,
                curiosity_level: data.curiosity_level
            }]);

            setAvatarState(data.avatar_state);
            setConfusionLevel(data.confusion_level);
            setCuriosityLevel(data.curiosity_level);

            if (data.layer_complete) {
                setRittyMessages(prev => [...prev, {
                    role: 'assistant',
                    content: '🎉 Wow! You explained it so well! I understand now! You can move to the next challenge!'
                }]);
            }
        } catch (err) {
            console.error('Ritty message failed:', err);
        } finally {
            setLoading(false);
        }
    };

    // Layer 2: Submit compression
    const handleCompressionSubmit = async () => {
        if (!session || !compressionInput.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post<CompressionEvaluation>('/feynman/layer2/compress', {
                session_id: session.session_id,
                word_limit: currentWordLimit,
                explanation: compressionInput
            });

            const data = response.data;
            setCompressionHistory(prev => [...prev, {
                limit: currentWordLimit,
                text: compressionInput,
                score: data.score,
                feedback: data.feedback,
                suggestion: data.suggestion
            }]);

            if (data.passed && data.next_word_limit) {
                setCurrentWordLimit(data.next_word_limit);
                setCompressionInput('');
            }
        } catch (err) {
            console.error('Compression submit failed:', err);
        } finally {
            setLoading(false);
        }
    };

    // Layer 3: Respond to Why Spiral
    const handleWhySpiralRespond = async (admitsUnknown: boolean = false) => {
        if (!session || (!whySpiralInput.trim() && !admitsUnknown)) return;

        const userMessage = admitsUnknown ? "I don't know..." : whySpiralInput;
        setWhySpiralInput('');
        setWhySpiralMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        setLoading(true);
        try {
            const response = await api.client.post<WhySpiralResponse>('/feynman/layer3/respond', {
                session_id: session.session_id,
                response: userMessage,
                admits_unknown: admitsUnknown
            });

            const data = response.data;
            setWhyDepth(data.current_depth);

            if (data.boundary_detected) {
                setBoundaryFound(true);
                setWhySpiralMessages(prev => [...prev, {
                    role: 'assistant',
                    content: `🎯 **Knowledge Boundary Found!**\n\n${data.boundary_topic ? `Topic: ${data.boundary_topic}` : ''}\n\n${data.exploration_offer || 'This is the edge of your current understanding. Great job exploring!'}`
                }]);
            } else if (data.next_question) {
                setWhySpiralMessages(prev => [...prev, {
                    role: 'assistant',
                    content: data.next_question || ''
                }]);
            }
        } catch (err) {
            console.error('Why spiral failed:', err);
        } finally {
            setLoading(false);
        }
    };

    // Layer 4: Submit analogy
    const handleAnalogySubmit = async () => {
        if (!session || !analogyInput.trim()) return;

        // Add user message to history
        const userEntry = { role: 'user', content: `[${analogyPhase}]: ${analogyInput}` };
        setAnalogyHistory(prev => [...prev, userEntry]);

        setLoading(true);
        try {
            const response = await api.client.post<AnalogyEvaluation>('/feynman/layer4/submit', {
                session_id: session.session_id,
                analogy_text: analogyInput,
                phase: analogyPhase
            });

            const data = response.data;
            setAnalogyFeedback(data);

            // Add AI response to history with image if present
            const assistantEntry = {
                role: 'assistant',
                content: `Score: ${'⭐'.repeat(data.score)}\nStrengths: ${data.strengths.join(', ')}\nWeaknesses: ${data.weaknesses.join(', ')}`,
                image_url: data.analogy_image_url
            };
            setAnalogyHistory(prev => [...prev, assistantEntry]);

            if (data.stress_test_question) {
                setStressTestQuestion(data.stress_test_question);
                setAnalogyPhase('defend');
            } else if (analogyPhase === 'defend') {
                setAnalogyPhase('refine');
            }
            setAnalogyInput('');
        } catch (err) {
            console.error('Analogy submit failed:', err);
        } finally {
            setLoading(false);
        }
    };

    // Layer 5: Explain to Lecture Hall
    const handleLectureExplain = async () => {
        if (!session || !lectureInput.trim()) return;

        const userMessage = lectureInput;
        setLectureInput('');
        setLectureMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        setLoading(true);
        try {
            const response = await api.client.post<LectureHallResponse>('/feynman/layer5/explain', {
                session_id: session.session_id,
                message: userMessage
            });

            const data = response.data;
            setPersonaFeedback(data.personas);

            // Build response message
            let responseContent = data.personas.map(p =>
                `**${p.persona_name}** ${p.is_satisfied ? '✅' : '❌'}\n${p.response}${p.follow_up_question ? '\n❓ ' + p.follow_up_question : ''}`
            ).join('\n\n');

            if (data.all_satisfied) {
                responseContent += '\n\n🎉 **All personas are satisfied!**';
            } else if (data.suggestion) {
                responseContent += `\n\n💡 **Suggestion:** ${data.suggestion}`;
            }

            setLectureMessages(prev => [...prev, { role: 'assistant', content: responseContent }]);
        } catch (err) {
            console.error('Lecture explain failed:', err);
        } finally {
            setLoading(false);
        }
    };

    // Complete session
    const handleCompleteSession = async () => {
        if (!session) return;

        setLoading(true);
        try {
            const response = await api.client.post(`/feynman/session/${session.session_id}/complete`);
            alert(`Session Complete!\n\nXP Earned: ${response.data.teaching_xp_earned}\nAchievements: ${response.data.achievements_unlocked.join(', ') || 'None'}`);
            setStep('setup');
            setSession(null);
        } catch (err) {
            console.error('Complete session failed:', err);
        } finally {
            setLoading(false);
        }
    };

    // Render Setup Screen
    if (step === 'setup') {
        return (
            <div className="max-w-2xl mx-auto space-y-6">
                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl p-8 text-white">
                    <h1 className="text-3xl font-bold mb-2">🧠 Feynman Technique</h1>
                    <p className="opacity-90">"If you can't explain it simply, you don't understand it."</p>
                    <p className="text-sm opacity-75 mt-2">— Richard Feynman</p>
                </div>

                <div className="bg-white rounded-xl p-6 shadow-lg space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">What do you want to teach?</label>
                        <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="e.g., How does photosynthesis work?"
                            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                        <select
                            value={subject}
                            onChange={(e) => setSubject(e.target.value)}
                            className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                        >
                            {subjects.map(s => <option key={s} value={s}>{s}</option>)}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty Level: {difficulty}</label>
                        <input
                            type="range"
                            min="1"
                            max="10"
                            value={difficulty}
                            onChange={(e) => setDifficulty(parseInt(e.target.value))}
                            className="w-full"
                        />
                        <div className="flex justify-between text-xs text-gray-500">
                            <span>Easy</span>
                            <span>Hard</span>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Start from Layer (optional)</label>
                        <div className="grid grid-cols-5 gap-2">
                            {layerNames.map(layer => (
                                <button
                                    key={layer.id}
                                    onClick={() => setStartingLayer(layer.id)}
                                    className={`p-2 rounded-lg border-2 text-center transition-all ${startingLayer === layer.id
                                        ? 'border-indigo-500 bg-indigo-50'
                                        : 'border-gray-200 hover:border-indigo-300'
                                        }`}
                                >
                                    <div className="text-2xl">{layer.emoji}</div>
                                    <div className="text-xs mt-1">{layer.name}</div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {error && (
                        <div className="text-red-500 text-sm">{error}</div>
                    )}

                    <button
                        onClick={handleStartSession}
                        disabled={loading}
                        className="w-full py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg font-bold hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50"
                    >
                        {loading ? 'Starting...' : '🚀 Start Teaching Session'}
                    </button>
                </div>

                {/* Session History Section - Collapsible */}
                <div className="bg-white rounded-xl p-4 shadow-lg">
                    <button
                        onClick={toggleHistory}
                        className="w-full flex items-center justify-between p-2 hover:bg-gray-50 rounded-lg transition-all"
                    >
                        <span className="text-lg font-semibold text-gray-700">
                            📚 Recent Teaching Sessions
                        </span>
                        <span className="text-gray-500 text-xl">
                            {showHistory ? '▲' : '▼'}
                        </span>
                    </button>
                    {showHistory && (
                        <div className="mt-4">
                            {historyLoading && <div className="text-center py-4 text-gray-500">⏳ Loading sessions...</div>}
                            {historyError && <div className="text-center py-4 text-red-500">{historyError}</div>}
                            {!historyLoading && !historyError && sessionHistory.length === 0 && (
                                <div className="text-center py-4 text-gray-500">No previous sessions. Start your first teaching session!</div>
                            )}
                            {!historyLoading && sessionHistory.length > 0 && (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                                    {sessionHistory.map((s, idx) => (
                                        <button
                                            key={s.id || idx}
                                            onClick={() => resumeSession(s)}
                                            className="p-4 rounded-lg border-2 border-gray-200 hover:border-indigo-400 hover:bg-indigo-50 text-left transition-all group"
                                        >
                                            <div className="flex items-start justify-between mb-2">
                                                <span className="text-xs px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded-full">{s.subject || 'General'}</span>
                                                <span className={`text-xs px-2 py-0.5 rounded-full ${s.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                                                    {s.status === 'completed' ? '✅ Done' : '🔄 In Progress'}
                                                </span>
                                            </div>
                                            <h4 className="font-semibold text-gray-800 group-hover:text-indigo-700 mb-1 line-clamp-2">{s.topic}</h4>
                                            <div className="flex items-center gap-2 text-xs text-gray-500">
                                                <span>Layer {s.current_layer || 1}</span>
                                                <span>•</span>
                                                <span>{new Date(s.started_at).toLocaleDateString()}</span>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        );
    }

                // Render Learning Screen
                return (
                <div className="max-w-6xl mx-auto space-y-4">
                    {/* Header with Layer Navigation */}
                    <div className="bg-white rounded-xl p-4 shadow-lg">
                        <div className="flex items-center justify-between mb-4">
                            <div>
                                <h1 className="text-xl font-bold text-gray-900">🧠 {session?.topic}</h1>
                                <p className="text-sm text-gray-500">{session?.subject}</p>
                            </div>
                            <button
                                onClick={handleCompleteSession}
                                className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                            >
                                ✅ Complete Session
                            </button>
                        </div>

                        {/* Layer Tabs */}
                        <div className="flex gap-2 overflow-x-auto pb-2">
                            {layerNames.map(layer => (
                                <button
                                    key={layer.id}
                                    onClick={() => handleChangeLayer(layer.id)}
                                    disabled={loading}
                                    className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-all cursor-pointer ${currentLayer === layer.id
                                        ? `bg-gradient-to-r ${layer.color} text-white shadow-lg scale-105`
                                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200 hover:scale-102'
                                        } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                                >
                                    <span>{layer.emoji}</span>
                                    <span className="font-medium">{layer.name}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Layer Content */}
                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
                        {/* Main Chat Area */}
                        <div className="lg:col-span-3 bg-white rounded-xl shadow-lg overflow-hidden">
                            {/* Layer 1: Ritty */}
                            {currentLayer === 1 && (
                                <>
                                    <div className={`bg-gradient-to-r ${layerNames[0].color} text-white p-4`}>
                                        <h2 className="font-bold">👦 Explain to Ritty</h2>
                                        <p className="text-sm opacity-80">An 8-year-old who wants to learn from you!</p>
                                    </div>
                                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                                        {rittyMessages.map((msg, idx) => (
                                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                                <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                                    ? 'bg-amber-500 text-white'
                                                    : 'bg-amber-50 text-gray-800 border border-amber-200'
                                                    }`}>
                                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(msg.content) }} />
                                                </div>
                                            </div>
                                        ))}
                                        {loading && <div className="text-center text-gray-500">Ritty is thinking... 🤔</div>}
                                        <div ref={chatEndRef} />
                                    </div>
                                    <div className="p-4 border-t flex gap-2">
                                        <input
                                            type="text"
                                            value={rittyInput}
                                            onChange={(e) => setRittyInput(e.target.value)}
                                            onKeyPress={(e) => e.key === 'Enter' && handleRittySend()}
                                            placeholder="Explain to Ritty..."
                                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
                                        />
                                        <button
                                            onClick={handleRittySend}
                                            disabled={loading}
                                            className="px-6 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 disabled:opacity-50"
                                        >
                                            Teach
                                        </button>
                                    </div>
                                </>
                            )}

                            {/* Layer 2: Compression */}
                            {currentLayer === 2 && (
                                <>
                                    <div className={`bg-gradient-to-r ${layerNames[1].color} text-white p-4`}>
                                        <h2 className="font-bold">📝 Compression Challenge</h2>
                                        <p className="text-sm opacity-80">Explain in {currentWordLimit} words or less!</p>
                                    </div>
                                    <div className="p-4 space-y-4">
                                        <div className="flex gap-2 justify-center">
                                            {[100, 50, 25, 15, 10, 1].map(limit => (
                                                <div
                                                    key={limit}
                                                    className={`px-3 py-1 rounded-full text-sm ${currentWordLimit === limit
                                                        ? 'bg-blue-500 text-white'
                                                        : compressionHistory.some(h => h.limit === limit)
                                                            ? 'bg-green-100 text-green-700'
                                                            : 'bg-gray-100 text-gray-500'
                                                        }`}
                                                >
                                                    {limit}
                                                </div>
                                            ))}
                                        </div>

                                        {compressionHistory.map((h, idx) => (
                                            <div key={idx} className="p-3 bg-gray-50 rounded-lg space-y-2">
                                                <div className="flex justify-between text-sm text-gray-500">
                                                    <span>{h.limit} words</span>
                                                    <span>Score: {h.score}/5 {'⭐'.repeat(h.score)}</span>
                                                </div>
                                                <p className="text-gray-800 italic">"{h.text}"</p>
                                                <div className="p-2 bg-blue-50 rounded border-l-4 border-blue-400">
                                                    <p className="text-sm text-blue-800">{h.feedback}</p>
                                                    {h.suggestion && (
                                                        <p className="text-xs text-blue-600 mt-1">💡 {h.suggestion}</p>
                                                    )}
                                                </div>
                                            </div>
                                        ))}

                                        <div>
                                            <textarea
                                                value={compressionInput}
                                                onChange={(e) => setCompressionInput(e.target.value)}
                                                placeholder={`Explain ${session?.topic} in ${currentWordLimit} words or less...`}
                                                className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 h-32"
                                            />
                                            <div className="flex justify-between items-center mt-2">
                                                <span className={`text-sm ${compressionInput.split(/\s+/).filter(Boolean).length > currentWordLimit ? 'text-red-500' : 'text-gray-500'}`}>
                                                    {compressionInput.split(/\s+/).filter(Boolean).length} / {currentWordLimit} words
                                                </span>
                                                <button
                                                    onClick={handleCompressionSubmit}
                                                    disabled={loading}
                                                    className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                                                >
                                                    Submit
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </>
                            )}

                            {/* Layer 3: Why Spiral */}
                            {currentLayer === 3 && (
                                <>
                                    <div className={`bg-gradient-to-r ${layerNames[2].color} text-white p-4`}>
                                        <h2 className="font-bold">🌀 Why Spiral - Depth {whyDepth}/5</h2>
                                        <p className="text-sm opacity-80">Answer "why" until you reach your knowledge boundary</p>
                                    </div>
                                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                                        {whySpiralMessages.map((msg, idx) => (
                                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                                <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                                    ? 'bg-purple-500 text-white'
                                                    : 'bg-purple-50 text-gray-800 border border-purple-200'
                                                    }`}>
                                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(msg.content) }} />
                                                </div>
                                            </div>
                                        ))}
                                        {loading && <div className="text-center text-gray-500">Thinking of the next question... 🌀</div>}
                                        <div ref={chatEndRef} />
                                    </div>
                                    <div className="p-4 border-t space-y-2">
                                        <div className="flex gap-2">
                                            <input
                                                type="text"
                                                value={whySpiralInput}
                                                onChange={(e) => setWhySpiralInput(e.target.value)}
                                                onKeyPress={(e) => e.key === 'Enter' && handleWhySpiralRespond(false)}
                                                placeholder="Explain why..."
                                                className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                                disabled={boundaryFound}
                                            />
                                            <button
                                                onClick={() => handleWhySpiralRespond(false)}
                                                disabled={loading || boundaryFound}
                                                className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:opacity-50"
                                            >
                                                Answer
                                            </button>
                                        </div>
                                        <button
                                            onClick={() => handleWhySpiralRespond(true)}
                                            disabled={loading || boundaryFound}
                                            className="text-sm text-purple-600 hover:underline"
                                        >
                                            🤷 I don't know (find my knowledge boundary)
                                        </button>
                                    </div>
                                </>
                            )}

                            {/* Layer 4: Analogy */}
                            {currentLayer === 4 && (
                                <>
                                    <div className={`bg-gradient-to-r ${layerNames[3].color} text-white p-4`}>
                                        <h2 className="font-bold">🎨 Analogy Architect - {analogyPhase.toUpperCase()}</h2>
                                        <p className="text-sm opacity-80">Create, defend, and refine your analogy</p>
                                    </div>
                                    <div className="p-4 space-y-4 h-[500px] overflow-y-auto">
                                        {/* Show history with images when returning to layer */}
                                        {analogyHistory.map((h, idx) => (
                                            <div key={idx} className={`flex ${h.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                                <div className={`max-w-[85%] p-3 rounded-lg ${h.role === 'user'
                                                    ? 'bg-green-500 text-white'
                                                    : 'bg-gray-50 text-gray-800 border'
                                                    }`}>
                                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(h.content) }} />
                                                    {h.image_url && (
                                                        <div className="mt-3 border rounded-lg overflow-hidden">
                                                            <div className="bg-green-100 px-2 py-1 text-xs text-green-800">
                                                                🎨 Analogy Visualization
                                                            </div>
                                                            <img
                                                                src={h.image_url.startsWith('data:') ? h.image_url : `${BACKEND_URL}${h.image_url}`}
                                                                alt="Analogy visualization"
                                                                className="w-full h-auto"
                                                                onError={(e) => (e.target as HTMLImageElement).style.display = 'none'}
                                                            />
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ))}

                                        {stressTestQuestion && analogyPhase === 'defend' && (
                                            <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                                                <p className="font-medium text-orange-800">🔥 Stress Test:</p>
                                                <p className="text-orange-700">{stressTestQuestion}</p>
                                            </div>
                                        )}

                                        {loading && <div className="text-center text-gray-500">Generating feedback... 🎨</div>}
                                        <div ref={chatEndRef} />

                                        <textarea
                                            value={analogyInput}
                                            onChange={(e) => setAnalogyInput(e.target.value)}
                                            placeholder={analogyPhase === 'create'
                                                ? `Create an analogy for "${session?.topic}"...`
                                                : analogyPhase === 'defend'
                                                    ? 'Defend your analogy against the stress test...'
                                                    : 'Refine your analogy based on the feedback...'
                                            }
                                            className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 h-32"
                                        />
                                        <button
                                            onClick={handleAnalogySubmit}
                                            disabled={loading}
                                            className="w-full py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50"
                                        >
                                            {analogyPhase === 'create' ? '✨ Create Analogy' : analogyPhase === 'defend' ? '🛡️ Defend' : '🔄 Refine'}
                                        </button>
                                    </div>
                                </>
                            )}

                            {/* Layer 5: Lecture Hall */}
                            {currentLayer === 5 && (
                                <>
                                    <div className={`bg-gradient-to-r ${layerNames[4].color} text-white p-4`}>
                                        <h2 className="font-bold">🎓 Lecture Hall</h2>
                                        <p className="text-sm opacity-80">Satisfy all 5 personas!</p>
                                    </div>
                                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                                        {lectureMessages.map((msg, idx) => (
                                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                                <div className={`max-w-[90%] p-3 rounded-lg ${msg.role === 'user'
                                                    ? 'bg-red-500 text-white'
                                                    : 'bg-gray-50 text-gray-800 border'
                                                    }`}>
                                                    <div dangerouslySetInnerHTML={{ __html: formatChatContent(msg.content) }} />
                                                </div>
                                            </div>
                                        ))}
                                        {loading && <div className="text-center text-gray-500">Personas are evaluating... 🎓</div>}
                                        <div ref={chatEndRef} />
                                    </div>
                                    <div className="p-4 border-t flex gap-2">
                                        <input
                                            type="text"
                                            value={lectureInput}
                                            onChange={(e) => setLectureInput(e.target.value)}
                                            onKeyPress={(e) => e.key === 'Enter' && handleLectureExplain()}
                                            placeholder="Explain to the audience..."
                                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                        />
                                        <button
                                            onClick={handleLectureExplain}
                                            disabled={loading}
                                            className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
                                        >
                                            Explain
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>

                        {/* Sidebar */}
                        <div className="space-y-4">
                            {/* Ritty Avatar (Layer 1) */}
                            {currentLayer === 1 && (
                                <div className="bg-white rounded-xl p-4 shadow-lg">
                                    <RittyAvatar state={avatarState} confusion={confusionLevel} curiosity={curiosityLevel} />
                                </div>
                            )}

                            {/* Persona Satisfaction (Layer 5) */}
                            {currentLayer === 5 && personaFeedback.length > 0 && (
                                <div className="bg-white rounded-xl p-4 shadow-lg space-y-3">
                                    <h3 className="font-bold text-gray-800">Persona Satisfaction</h3>
                                    {personaFeedback.map(p => (
                                        <div key={p.persona} className="flex items-center gap-2">
                                            <span className={`text-lg ${p.is_satisfied ? '' : 'opacity-50'}`}>
                                                {p.is_satisfied ? '✅' : '❌'}
                                            </span>
                                            <div className="flex-1">
                                                <div className="text-sm font-medium">{p.persona_name}</div>
                                                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                                    <div
                                                        className={`h-full transition-all ${p.satisfaction > 0.7 ? 'bg-green-500' : p.satisfaction > 0.4 ? 'bg-yellow-500' : 'bg-red-500'}`}
                                                        style={{ width: `${p.satisfaction * 100}%` }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}

                            {/* Tips */}
                            <div className="bg-white rounded-xl p-4 shadow-lg">
                                <h3 className="font-bold text-gray-800 mb-2">💡 Tips</h3>
                                <ul className="text-sm text-gray-600 space-y-1">
                                    {currentLayer === 1 && (
                                        <>
                                            <li>• Use simple words Ritty can understand</li>
                                            <li>• Give examples from everyday life</li>
                                            <li>• Watch the confusion meter!</li>
                                        </>
                                    )}
                                    {currentLayer === 2 && (
                                        <>
                                            <li>• Focus on the core concept</li>
                                            <li>• Remove unnecessary words</li>
                                            <li>• Each round halves the limit!</li>
                                        </>
                                    )}
                                    {currentLayer === 3 && (
                                        <>
                                            <li>• Think deeply about causation</li>
                                            <li>• It's okay to say "I don't know"</li>
                                            <li>• Finding gaps = learning opportunities!</li>
                                        </>
                                    )}
                                    {currentLayer === 4 && (
                                        <>
                                            <li>• Good analogies are relatable</li>
                                            <li>• Consider where it might break down</li>
                                            <li>• Defend against stress tests!</li>
                                        </>
                                    )}
                                    {currentLayer === 5 && (
                                        <>
                                            <li>• Balance depth with accessibility</li>
                                            <li>• Include practical examples</li>
                                            <li>• Satisfy ALL personas!</li>
                                        </>
                                    )}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                );
};
