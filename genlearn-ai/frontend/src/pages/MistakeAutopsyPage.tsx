import React, { useState, useRef, useEffect } from 'react';
import api, { BACKEND_URL } from '../services/api';
import { formatChatContent } from '../utils/helpers';

interface Diagnosis {
    most_likely_error: string;
    confidence: string;
    error_category: string;
    thought_process_reconstruction: string;
    misconception_identified: string;
}

interface Remediation {
    quick_fix: string;
    practice_problems: { question: string; focus: string }[];
}

interface AnalysisResult {
    diagnosis: Diagnosis;
    message: string;
    remediation: Remediation;
    encouragement: string;
    imageUrl?: string;
}

interface MCTMessage {
    role: 'user' | 'assistant';
    content: string;
    phase?: string;
    diagnosticQuestion?: string;
    imageUrl?: string;
}

interface CascadeTracking {
    surface_error: string;
    tested_prerequisites: string[];
    broken_link_found: boolean;
    root_misconception: string | null;
    repair_progress: string[];
}

export const MistakeAutopsyPage: React.FC = () => {
    const [mode, setMode] = useState<'input' | 'basic_result' | 'mct_chat'>('input');
    const [question, setQuestion] = useState('');
    const [correctAnswer, setCorrectAnswer] = useState('');
    const [studentAnswer, setStudentAnswer] = useState('');
    const [subject, setSubject] = useState('Mathematics');
    const [topic, setTopic] = useState('');
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState(false);

    // MCT Chat State
    const [mctMessages, setMctMessages] = useState<MCTMessage[]>([]);
    const [mctInput, setMctInput] = useState('');
    const [mctSessionId, setMctSessionId] = useState<string | null>(null);
    const [currentPhase, setCurrentPhase] = useState('surface_capture');
    const [mctTurnNumber, setMctTurnNumber] = useState(1);
    const [cascadeTracking, setCascadeTracking] = useState<CascadeTracking>({
        surface_error: '',
        tested_prerequisites: [],
        broken_link_found: false,
        root_misconception: null,
        repair_progress: []
    });
    const chatEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [mctMessages]);

    // History Section States - SAFE: Click-to-load, no blocking
    const [showHistorySources, setShowHistorySources] = useState(false);
    const [historyLoading, setHistoryLoading] = useState(false);
    const [selectedHistoryItem, setSelectedHistoryItem] = useState<any | null>(null);

    // Independent source states (each can fail independently)
    const [feynmanHistory, setFeynmanHistory] = useState<any[]>([]);
    const [learningHistory, setLearningHistory] = useState<any[]>([]);
    const [sessionsHistory, setSessionsHistory] = useState<any[]>([]);
    const [mctHistory, setMctHistory] = useState<any[]>([]);

    // Loaded conversation for chat-based analysis
    const [loadedConversation, setLoadedConversation] = useState<any[]>([]);
    const [inputMode, setInputMode] = useState<'manual' | 'chat'>('manual');
    const [conversationLoading, setConversationLoading] = useState(false);

    // Toggle and load history sources
    const toggleHistorySources = () => {
        if (!showHistorySources && feynmanHistory.length === 0 && mctHistory.length === 0) {
            loadAllHistory();
        }
        setShowHistorySources(!showHistorySources);
    };

    // Load all history sources in parallel with independent error handling
    const loadAllHistory = async () => {
        setHistoryLoading(true);
        await Promise.allSettled([
            loadFeynmanHistory(),
            loadLearningHistory(),
            loadSessionsHistory(),
            loadMctHistory()
        ]);
        setHistoryLoading(false);
    };

    // Load Feynman sessions
    const loadFeynmanHistory = async () => {
        try {
            const res = await api.client.get('/feynman/sessions/user/guest?limit=10');
            setFeynmanHistory(res.data.sessions || []);
        } catch (err) {
            console.error('Failed to load Feynman history:', err);
            setFeynmanHistory([]);
        }
    };

    // Load Learning history
    const loadLearningHistory = async () => {
        try {
            const res = await api.client.get('/learning/sessions?limit=10');
            setLearningHistory(res.data.sessions || res.data || []);
        } catch (err) {
            console.error('Failed to load Learning history:', err);
            setLearningHistory([]);
        }
    };

    // Load general sessions history
    const loadSessionsHistory = async () => {
        try {
            const res = await api.client.get('/sessions?limit=10');
            setSessionsHistory(res.data.sessions || res.data || []);
        } catch (err) {
            console.error('Failed to load Sessions history:', err);
            setSessionsHistory([]);
        }
    };

    // Load MCT/Mistake Autopsy sessions history
    const loadMctHistory = async () => {
        try {
            const res = await api.client.get('/features/mct/sessions/user/guest?limit=10');
            setMctHistory(res.data.sessions || []);
        } catch (err) {
            console.error('Failed to load MCT history:', err);
            setMctHistory([]);
        }
    };

    // Select history item and pre-fill form - fetches conversation for Feynman
    const selectHistoryItem = async (item: any, source: string) => {
        setSelectedHistoryItem({ ...item, source });

        // Pre-fill form based on source
        setQuestion(item.topic || item.original_question || item.name || '');
        setSubject(item.subject || 'Mathematics');
        setTopic(item.topic || '');

        // For MCT items, DIRECTLY RESUME the session (enter chat mode)
        if (source === 'mct') {
            setStudentAnswer(item.student_answer || '');
            setCorrectAnswer(item.correct_answer || '');
            setLoadedConversation([]);
            setInputMode('manual');

            // Resume the MCT session directly
            setMctSessionId(item.id);
            setCurrentPhase(item.phase || 'surface_capture');

            // Fetch conversation history for this session
            try {
                const historyRes = await api.client.get(`/features/mct/conversation/${item.id}`);
                const messages = historyRes.data.messages || [];

                if (messages.length > 0) {
                    // Load previous messages including images
                    const loadedMessages = messages.map((m: any) => ({
                        role: m.role,
                        content: m.message,
                        phase: m.phase,
                        imageUrl: m.image_path || undefined  // Just pass the path, display code handles URL
                    }));

                    // Add welcome back message at the end
                    loadedMessages.push({
                        role: 'assistant',
                        content: `Welcome back! Here's our previous discussion. You can continue from where we left off.`,
                        phase: item.phase
                    });

                    setMctMessages(loadedMessages);
                } else {
                    // No previous messages, show welcome message
                    setMctMessages([{
                        role: 'assistant',
                        content: `Welcome back! Let's continue analyzing your answer about "${item.topic || item.original_question?.slice(0, 50)}". Tell me more about your understanding!`,
                        phase: item.phase
                    }]);
                }
            } catch (err) {
                console.error('Failed to load MCT history:', err);
                // Fallback welcome message
                setMctMessages([{
                    role: 'assistant',
                    content: `Welcome back! Let's continue analyzing your answer about "${item.topic || item.original_question?.slice(0, 50)}".`,
                    phase: item.phase
                }]);
            }

            // Enter chat mode directly
            setMode('mct_chat');
            return;
        }

        // For learning and sessions sources, pre-fill with helpful defaults
        if (source === 'learning' || source === 'sessions') {
            // These sessions don't have student answers stored, but we can use the topic
            // to let users do a quick analysis based on the topic
            setStudentAnswer(`[Review my understanding of: ${item.topic || 'this topic'}]`);
            setCorrectAnswer(`[Analyze my learning from this session]`);
            setLoadedConversation([]);
            setInputMode('manual');
            return;
        }

        // Clear answers for other sources
        setStudentAnswer('');
        setCorrectAnswer('');

        // For Feynman sessions, fetch full conversation
        if (source === 'feynman' && item.id) {
            setConversationLoading(true);
            try {
                const res = await api.client.get(`/feynman/session/${item.id}/full`);
                const allMessages = res.data.all_messages || [];
                setLoadedConversation(allMessages);
                setInputMode('chat');
            } catch (err) {
                console.error('Failed to load conversation:', err);
                setLoadedConversation([]);
                setInputMode('manual');
            } finally {
                setConversationLoading(false);
            }
        } else {
            setLoadedConversation([]);
            setInputMode('manual');
        }
    };

    const handleBasicAnalyze = async () => {
        // Chat mode - analyze the loaded conversation
        if (inputMode === 'chat' && loadedConversation.length > 0) {
            // Extract user messages as the "student's answer/explanation"
            const userMessages = loadedConversation
                .filter(m => m.role === 'user')
                .map(m => m.message)
                .join('\n');

            // Extract AI feedback as context (contains identified mistakes/weaknesses)
            const aiFeedback = loadedConversation
                .filter(m => m.role === 'assistant')
                .map(m => m.message)
                .join('\n');

            if (!userMessages.trim()) {
                alert('No user messages found in the conversation.');
                return;
            }

            setLoading(true);
            try {
                const response = await api.client.post('/features/mistake/analyze', {
                    question: `Analyze this learning conversation about: ${question}`,
                    correct_answer: `The AI already identified these issues:\n${aiFeedback.substring(0, 500)}`,
                    student_answer: userMessages,
                    subject,
                    topic: topic || subject
                });

                setResult(response.data);
                setMode('basic_result');
            } catch (err) {
                console.error('Analysis failed:', err);
                alert('Failed to analyze conversation. Please try again.');
            } finally {
                setLoading(false);
            }
            return;
        }

        // Manual mode - original behavior
        if (!question.trim() || !correctAnswer.trim() || !studentAnswer.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post('/features/mistake/analyze', {
                question,
                correct_answer: correctAnswer,
                student_answer: studentAnswer,
                subject,
                topic: topic || subject
            });

            setResult(response.data);
            setMode('basic_result');
        } catch (err) {
            console.error('Analysis failed:', err);
            alert('Failed to analyze mistake. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleStartMCT = async () => {
        // Chat mode - analyze loaded conversation with MCT
        if (inputMode === 'chat' && loadedConversation.length > 0) {
            const userMessages = loadedConversation
                .filter(m => m.role === 'user')
                .map(m => m.message)
                .join('\n');

            const aiFeedback = loadedConversation
                .filter(m => m.role === 'assistant')
                .map(m => m.message)
                .join('\n');

            if (!userMessages.trim()) {
                alert('No user messages found in the conversation.');
                return;
            }

            setLoading(true);
            try {
                const response = await api.client.post('/features/mct/start', {
                    question: `Deep analysis of learning conversation about: ${question}`,
                    correct_answer: `AI feedback context:\n${aiFeedback.substring(0, 500)}`,
                    student_answer: userMessages,
                    subject,
                    topic: topic || subject
                });

                setMctSessionId(response.data.session_id);
                setCurrentPhase(response.data.phase || 'surface_capture');
                setCascadeTracking(response.data.cascade_tracking || cascadeTracking);

                setMctMessages([{
                    role: 'assistant',
                    content: response.data.message || "Let's explore the conversation and find the root cause...",
                    phase: response.data.phase,
                    diagnosticQuestion: response.data.diagnostic_question
                }]);

                setMode('mct_chat');
            } catch (err) {
                console.error('MCT start failed:', err);
                alert('Failed to start MCT session. Please try again.');
            } finally {
                setLoading(false);
            }
            return;
        }

        // Manual mode - original behavior
        if (!question.trim() || !correctAnswer.trim() || !studentAnswer.trim()) return;

        setLoading(true);
        try {
            const response = await api.client.post('/features/mct/start', {
                question,
                correct_answer: correctAnswer,
                student_answer: studentAnswer,
                subject,
                topic: topic || subject
            });

            setMctSessionId(response.data.session_id);
            setCurrentPhase(response.data.phase || 'surface_capture');
            setCascadeTracking(response.data.cascade_tracking || cascadeTracking);

            setMctMessages([{
                role: 'assistant',
                content: response.data.message || "Let's explore what happened with your answer...",
                phase: response.data.phase,
                diagnosticQuestion: response.data.diagnostic_question
            }]);

            setMode('mct_chat');
        } catch (err) {
            console.error('MCT start failed:', err);
            alert('Failed to start MCT session. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleMCTSend = async () => {
        if (!mctInput.trim()) return;

        const userMessage = mctInput;
        setMctInput('');
        setMctMessages(prev => [...prev, { role: 'user', content: userMessage }]);

        setLoading(true);
        try {
            // Build conversation history for context
            const conversationHistory = mctMessages.map(m => ({
                role: m.role,
                content: m.content
            }));

            const response = await api.client.post('/features/mct/chat', {
                question,
                correct_answer: correctAnswer,
                student_answer: studentAnswer,
                subject,
                topic: topic || subject,
                user_message: userMessage,
                session_id: mctSessionId,
                conversation_history: conversationHistory,
                phase: currentPhase,
                cascade_tracking: cascadeTracking,
                turn_number: mctTurnNumber
            });

            // Update phase and tracking
            if (response.data.phase) setCurrentPhase(response.data.phase);
            if (response.data.cascade_tracking) setCascadeTracking(response.data.cascade_tracking);

            // Increment turn number for next message
            setMctTurnNumber(prev => prev + 1);

            setMctMessages(prev => [...prev, {
                role: 'assistant',
                content: response.data.message || "I see...",
                phase: response.data.phase,
                diagnosticQuestion: response.data.diagnostic_question,
                imageUrl: response.data.image  // Base64 image from backend
            }]);
        } catch (err) {
            console.error('MCT chat failed:', err);
            setMctMessages(prev => [...prev, {
                role: 'assistant',
                content: "I encountered an issue. Let's try that again."
            }]);
        } finally {
            setLoading(false);
        }
    };

    const getPhaseLabel = (phase: string) => {
        const phases: Record<string, { label: string; color: string; icon: string }> = {
            'surface_capture': { label: 'Analyzing', color: 'bg-blue-500', icon: '🔍' },
            'diagnostic_probing': { label: 'Probing', color: 'bg-yellow-500', icon: '🧐' },
            'root_found': { label: 'Root Found!', color: 'bg-orange-500', icon: '🎯' },
            'remediation': { label: 'Repairing', color: 'bg-green-500', icon: '🔧' },
            'verification': { label: 'Verifying', color: 'bg-purple-500', icon: '✅' }
        };
        return phases[phase] || { label: phase, color: 'bg-gray-500', icon: '📝' };
    };

    const resetToInput = () => {
        setMode('input');
        setResult(null);
        setMctMessages([]);
        setMctSessionId(null);
        setCurrentPhase('surface_capture');
        setCascadeTracking({
            surface_error: '',
            tested_prerequisites: [],
            broken_link_found: false,
            root_misconception: null,
            repair_progress: []
        });
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-lg">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">🔬 Mistake Autopsy + MCT</h1>
                <p className="text-gray-600">
                    Understand WHY you made a mistake and trace it to its root cause!
                </p>
            </div>

            {mode === 'input' && (
                <div className="bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl p-6">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">Enter the Mistake Details</h2>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Question</label>
                            <textarea
                                value={question}
                                onChange={(e) => setQuestion(e.target.value)}
                                placeholder="e.g., Solve: x² + 5x + 6 = 0"
                                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                rows={2}
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Your Answer</label>
                                <input
                                    type="text"
                                    value={studentAnswer}
                                    onChange={(e) => setStudentAnswer(e.target.value)}
                                    placeholder="e.g., x = -2, x = -4"
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Correct Answer</label>
                                <input
                                    type="text"
                                    value={correctAnswer}
                                    onChange={(e) => setCorrectAnswer(e.target.value)}
                                    placeholder="e.g., x = -2, x = -3"
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                                <select
                                    value={subject}
                                    onChange={(e) => setSubject(e.target.value)}
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                >
                                    <option>Mathematics</option>
                                    <option>Physics</option>
                                    <option>Chemistry</option>
                                    <option>Biology</option>
                                    <option>History</option>
                                    <option>Geography</option>
                                    <option>English</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Topic (Optional)</label>
                                <input
                                    type="text"
                                    value={topic}
                                    onChange={(e) => setTopic(e.target.value)}
                                    placeholder="e.g., Quadratic Equations"
                                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                                />
                            </div>
                        </div>

                        {/* Two Analysis Options */}
                        <div className="grid grid-cols-2 gap-4 pt-4">
                            <button
                                onClick={handleBasicAnalyze}
                                disabled={loading || (inputMode === 'manual' && (!question || !correctAnswer || !studentAnswer)) || (inputMode === 'chat' && loadedConversation.length === 0)}
                                className="py-3 bg-gradient-to-r from-teal-500 to-cyan-500 text-white rounded-lg font-bold hover:from-teal-600 hover:to-cyan-600 disabled:opacity-50"
                            >
                                {loading ? '🔬 Analyzing...' : '🔬 Quick Autopsy'}
                            </button>
                            <button
                                onClick={handleStartMCT}
                                disabled={loading || (inputMode === 'manual' && (!question || !correctAnswer || !studentAnswer)) || (inputMode === 'chat' && loadedConversation.length === 0)}
                                className="py-3 bg-gradient-to-r from-purple-500 to-indigo-500 text-white rounded-lg font-bold hover:from-purple-600 hover:to-indigo-600 disabled:opacity-50"
                            >
                                {loading ? '🧠 Starting...' : '🧠 Deep MCT Session'}
                            </button>
                        </div>
                        <p className="text-sm text-gray-500 text-center">
                            <strong>Quick Autopsy:</strong> Fast single analysis | <strong>MCT Session:</strong> Interactive deep-dive to root cause
                        </p>

                        {/* History Sources Section - Collapsible */}
                        <div className="mt-6 pt-4 border-t border-gray-200">
                            <button
                                onClick={toggleHistorySources}
                                className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-all"
                            >
                                <span className="font-medium text-gray-700">
                                    📂 Load from Previous Sessions
                                </span>
                                <span className="text-gray-500 text-lg">
                                    {showHistorySources ? '▲' : '▼'}
                                </span>
                            </button>

                            {showHistorySources && (
                                <div className="mt-4">
                                    {historyLoading && (
                                        <div className="text-center py-4 text-gray-500">
                                            ⏳ Loading history from all sources...
                                        </div>
                                    )}

                                    {selectedHistoryItem && (
                                        <div className="mb-4 p-3 bg-teal-50 border border-teal-200 rounded-lg">
                                            <span className="text-teal-700 font-medium">
                                                ✅ Selected: "{selectedHistoryItem.topic || selectedHistoryItem.name}" from {selectedHistoryItem.source}
                                            </span>
                                        </div>
                                    )}

                                    {/* Conversation Preview - Shows loaded chat history */}
                                    {conversationLoading && (
                                        <div className="mb-4 p-4 bg-gray-50 rounded-lg text-center">
                                            <span className="text-gray-500">⏳ Loading conversation...</span>
                                        </div>
                                    )}

                                    {loadedConversation.length > 0 && !conversationLoading && (
                                        <div className="mb-4 bg-gray-50 rounded-lg p-4">
                                            <h4 className="font-bold text-gray-700 mb-3 flex items-center gap-2">
                                                💬 Conversation Preview
                                                <span className="text-xs font-normal text-gray-500">({loadedConversation.length} messages)</span>
                                            </h4>
                                            <div className="max-h-48 overflow-y-auto space-y-2">
                                                {loadedConversation.slice(0, 10).map((msg, idx) => (
                                                    <div
                                                        key={idx}
                                                        className={`p-2 rounded text-sm ${msg.role === 'user'
                                                            ? 'bg-blue-50 border-l-4 border-blue-400'
                                                            : 'bg-gray-100 border-l-4 border-gray-400'
                                                            }`}
                                                    >
                                                        <span className="text-xs font-bold text-gray-600">
                                                            {msg.role === 'user' ? '👤 You' : '🤖 AI'}
                                                            {msg.layer && <span className="ml-1 text-gray-400">(Layer {msg.layer})</span>}
                                                        </span>
                                                        <p className="text-gray-700 mt-1 line-clamp-3">{msg.message}</p>
                                                    </div>
                                                ))}
                                                {loadedConversation.length > 10 && (
                                                    <p className="text-xs text-gray-400 text-center">
                                                        ... and {loadedConversation.length - 10} more messages
                                                    </p>
                                                )}
                                            </div>
                                            <p className="text-xs text-green-600 mt-2 font-medium">
                                                ✓ Click "Quick Autopsy" or "Deep MCT" to analyze this conversation for mistakes!
                                            </p>
                                        </div>
                                    )}

                                    {/* Horizontal Scroll Container */}
                                    <div className="overflow-x-auto pb-4">
                                        <div className="flex gap-4 min-w-max">
                                            {/* Feynman Sessions Column */}
                                            <div className="w-64 flex-shrink-0 bg-white border rounded-lg shadow-sm">
                                                <div className="p-3 bg-gradient-to-r from-amber-100 to-orange-100 rounded-t-lg">
                                                    <h4 className="font-bold text-amber-800">🧠 Feynman Sessions</h4>
                                                </div>
                                                <div className="p-2 max-h-48 overflow-y-auto">
                                                    {feynmanHistory.length === 0 ? (
                                                        <p className="text-sm text-gray-400 p-2">No sessions found</p>
                                                    ) : (
                                                        feynmanHistory.map((item, idx) => (
                                                            <button
                                                                key={item.id || idx}
                                                                onClick={() => selectHistoryItem(item, 'feynman')}
                                                                className={`w-full text-left p-2 rounded hover:bg-amber-50 transition-all text-sm ${selectedHistoryItem?.source === 'feynman' && selectedHistoryItem?.id === item.id
                                                                    ? 'bg-amber-100 border border-amber-300'
                                                                    : ''
                                                                    }`}
                                                            >
                                                                <div className="font-medium text-gray-800 truncate">{item.topic}</div>
                                                                <div className="text-xs text-gray-500">{item.subject} • Layer {item.current_layer || 1}</div>
                                                            </button>
                                                        ))
                                                    )}
                                                </div>
                                            </div>

                                            {/* Learning History Column */}
                                            <div className="w-64 flex-shrink-0 bg-white border rounded-lg shadow-sm">
                                                <div className="p-3 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-t-lg">
                                                    <h4 className="font-bold text-blue-800">📚 Learning History</h4>
                                                </div>
                                                <div className="p-2 max-h-48 overflow-y-auto">
                                                    {learningHistory.length === 0 ? (
                                                        <p className="text-sm text-gray-400 p-2">No history found</p>
                                                    ) : (
                                                        learningHistory.map((item, idx) => (
                                                            <button
                                                                key={item.id || idx}
                                                                onClick={() => selectHistoryItem(item, 'learning')}
                                                                className={`w-full text-left p-2 rounded hover:bg-blue-50 transition-all text-sm ${selectedHistoryItem?.source === 'learning' && selectedHistoryItem?.id === item.id
                                                                    ? 'bg-blue-100 border border-blue-300'
                                                                    : ''
                                                                    }`}
                                                            >
                                                                <div className="font-medium text-gray-800 truncate">{item.topic || item.question || item.title}</div>
                                                                <div className="text-xs text-gray-500">{item.subject || 'General'}</div>
                                                            </button>
                                                        ))
                                                    )}
                                                </div>
                                            </div>

                                            {/* General Sessions Column */}
                                            <div className="w-64 flex-shrink-0 bg-white border rounded-lg shadow-sm">
                                                <div className="p-3 bg-gradient-to-r from-purple-100 to-indigo-100 rounded-t-lg">
                                                    <h4 className="font-bold text-purple-800">🎯 Past Sessions</h4>
                                                </div>
                                                <div className="p-2 max-h-48 overflow-y-auto">
                                                    {sessionsHistory.length === 0 ? (
                                                        <p className="text-sm text-gray-400 p-2">No sessions found</p>
                                                    ) : (
                                                        sessionsHistory.map((item, idx) => (
                                                            <button
                                                                key={item.id || idx}
                                                                onClick={() => selectHistoryItem(item, 'sessions')}
                                                                className={`w-full text-left p-2 rounded hover:bg-purple-50 transition-all text-sm ${selectedHistoryItem?.source === 'sessions' && selectedHistoryItem?.id === item.id
                                                                    ? 'bg-purple-100 border border-purple-300'
                                                                    : ''
                                                                    }`}
                                                            >
                                                                <div className="font-medium text-gray-800 truncate">{item.topic || item.name || item.title}</div>
                                                                <div className="text-xs text-gray-500">{item.subject || 'General'}</div>
                                                            </button>
                                                        ))
                                                    )}
                                                </div>
                                            </div>

                                            {/* MCT History Column - Resume past analyses */}
                                            <div className="w-64 flex-shrink-0 bg-white border rounded-lg shadow-sm">
                                                <div className="p-3 bg-gradient-to-r from-red-100 to-pink-100 rounded-t-lg">
                                                    <h4 className="font-bold text-red-800">🔬 MCT History</h4>
                                                </div>
                                                <div className="p-2 max-h-48 overflow-y-auto">
                                                    {mctHistory.length === 0 ? (
                                                        <p className="text-sm text-gray-400 p-2">No MCT sessions found</p>
                                                    ) : (
                                                        mctHistory.map((item, idx) => (
                                                            <button
                                                                key={item.id || idx}
                                                                onClick={() => selectHistoryItem(item, 'mct')}
                                                                className={`w-full text-left p-2 rounded hover:bg-red-50 transition-all text-sm ${selectedHistoryItem?.source === 'mct' && selectedHistoryItem?.id === item.id
                                                                    ? 'bg-red-100 border border-red-300'
                                                                    : ''
                                                                    }`}
                                                            >
                                                                <div className="font-medium text-gray-800 truncate">{item.topic || item.original_question?.slice(0, 30)}</div>
                                                                <div className="text-xs text-gray-500">{item.subject || 'General'} • {item.phase || 'In Progress'}</div>
                                                            </button>
                                                        ))
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Basic Result Mode */}
            {mode === 'basic_result' && result && (
                <div className="space-y-4">
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <h3 className="text-xl font-bold text-red-600 mb-4">🐛 Bug Found in Your Brain!</h3>
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                            <p className="font-medium text-red-800">Error Type: {result.diagnosis?.error_category || 'Unknown'}</p>
                            <p className="text-red-700 mt-1">{result.diagnosis?.most_likely_error}</p>
                        </div>
                        {result.diagnosis?.misconception_identified && (
                            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                                <p className="font-medium text-orange-800">The Wrong Belief:</p>
                                <p className="text-orange-700 mt-1">{result.diagnosis.misconception_identified}</p>
                            </div>
                        )}
                    </div>

                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="text-xl font-bold text-gray-800">📝 Explanation</h3>
                            <button
                                onClick={handleStartMCT}
                                className="px-4 py-2 bg-purple-500 text-white rounded-lg text-sm hover:bg-purple-600"
                            >
                                🧠 Go Deeper with MCT
                            </button>
                        </div>
                        <div
                            className="prose prose-sm max-w-none"
                            dangerouslySetInnerHTML={{
                                __html: formatChatContent(result.message || '')
                            }}
                        />
                    </div>

                    <button onClick={resetToInput} className="w-full py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
                        ← Try Another Problem
                    </button>
                </div>
            )}

            {/* MCT Chat Mode */}
            {mode === 'mct_chat' && (
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    {/* Header with Phase Progress */}
                    <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-4">
                        <div className="flex justify-between items-center">
                            <div>
                                <h2 className="font-bold">🧠 Misconception Cascade Tracing</h2>
                                <p className="text-sm opacity-80 truncate max-w-md">{question}</p>
                            </div>
                            <div className="text-right">
                                <div className={`px-3 py-1 rounded-full text-sm ${getPhaseLabel(currentPhase).color}`}>
                                    {getPhaseLabel(currentPhase).icon} {getPhaseLabel(currentPhase).label}
                                </div>
                            </div>
                        </div>

                        {/* Cascade Progress Bar */}
                        <div className="mt-3 flex gap-1">
                            {['surface_capture', 'diagnostic_probing', 'root_found', 'remediation', 'verification'].map((phase, idx) => (
                                <div
                                    key={phase}
                                    className={`h-2 flex-1 rounded ${['surface_capture', 'diagnostic_probing', 'root_found', 'remediation', 'verification']
                                        .indexOf(currentPhase) >= idx
                                        ? 'bg-white'
                                        : 'bg-white/30'
                                        }`}
                                />
                            ))}
                        </div>
                    </div>

                    {/* Root Found Banner */}
                    {cascadeTracking.broken_link_found && cascadeTracking.root_misconception && (
                        <div className="bg-orange-100 border-b border-orange-200 p-3 text-center">
                            <p className="text-orange-800 font-medium">
                                🎯 Root Misconception Found: <strong>{cascadeTracking.root_misconception}</strong>
                            </p>
                        </div>
                    )}

                    {/* Chat Messages */}
                    <div className="h-96 overflow-y-auto p-4 space-y-4">
                        {mctMessages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                                    ? 'bg-purple-500 text-white'
                                    : 'bg-gray-100 text-gray-800'
                                    }`}>
                                    <div dangerouslySetInnerHTML={{
                                        __html: formatChatContent(msg.content)
                                    }} />

                                    {msg.diagnosticQuestion && msg.role === 'assistant' && (
                                        <div className="mt-2 pt-2 border-t border-gray-200">
                                            <p className="text-sm font-medium text-purple-700">
                                                🤔 {msg.diagnosticQuestion}
                                            </p>
                                        </div>
                                    )}

                                    {msg.imageUrl && (
                                        <img
                                            src={msg.imageUrl.startsWith('data:') ? msg.imageUrl : `${BACKEND_URL}${msg.imageUrl}`}
                                            alt="Explanation"
                                            className="mt-2 rounded-lg max-w-full max-h-64"
                                        />
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-gray-100 p-3 rounded-lg animate-pulse">
                                    🧠 Analyzing your thinking...
                                </div>
                            </div>
                        )}
                        <div ref={chatEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-4 border-t flex gap-2">
                        <input
                            type="text"
                            value={mctInput}
                            onChange={(e) => setMctInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleMCTSend()}
                            placeholder="Answer the question or explain your thinking..."
                            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                            disabled={loading}
                        />
                        <button
                            onClick={handleMCTSend}
                            disabled={loading || !mctInput.trim()}
                            className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 disabled:opacity-50"
                        >
                            Send
                        </button>
                    </div>

                    {/* Footer with Reset */}
                    <div className="p-2 border-t bg-gray-50 text-center">
                        <button onClick={resetToInput} className="text-sm text-gray-500 hover:text-gray-700">
                            ← Start Over with New Problem
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
