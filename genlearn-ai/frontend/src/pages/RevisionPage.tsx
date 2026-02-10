import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api, { BACKEND_URL } from '../services/api';
import { SceneDisplay } from '../components/learning/SceneDisplay';

interface TextOverlay {
    text: string;
    position: 'top' | 'center' | 'bottom';
    style: 'speech_bubble' | 'caption' | 'dramatic';
}

interface QuizOption {
    key: string;
    text: string;
}

interface Quiz {
    question_id: string;
    question_text: string;
    options: QuizOption[];
    correct_answers: string[];
    explanation: string;
    is_multi_select: boolean;
    points: number;
}

interface StorySegment {
    segment_number: number;
    narrative: string;
    scene_description: string;
    scene_image_url: string;
    text_overlay: TextOverlay;
    quiz: Quiz;
}

interface SessionRevision {
    session_id: string;
    topic: string;
    difficulty_level: number;
    duration_minutes: number;
    story_style: string;
    visual_style: string;
    score: number;
    status: string;
    started_at: string;
    completed_at: string;
    story_segments: StorySegment[];
    total_segments: number;
}

export const RevisionPage: React.FC = () => {
    const { sessionId } = useParams<{ sessionId: string }>();
    const navigate = useNavigate();
    const [session, setSession] = useState<SessionRevision | null>(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showQuiz, setShowQuiz] = useState(false);
    const [showAnswer, setShowAnswer] = useState(false);

    useEffect(() => {
        if (sessionId) {
            loadSession();
        }
    }, [sessionId]);

    const loadSession = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await api.getSessionRevision(sessionId!);
            setSession(response);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load session');
        } finally {
            setLoading(false);
        }
    };

    const currentSegment = session?.story_segments[currentIndex];

    const handleNext = () => {
        if (session && currentIndex < session.story_segments.length - 1) {
            setCurrentIndex(prev => prev + 1);
            setShowQuiz(false);
            setShowAnswer(false);
        }
    };

    const handlePrev = () => {
        if (currentIndex > 0) {
            setCurrentIndex(prev => prev - 1);
            setShowQuiz(false);
            setShowAnswer(false);
        }
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mb-4"></div>
                <p className="text-gray-600">Loading session for revision...</p>
            </div>
        );
    }

    if (error || !session) {
        return (
            <div className="bg-red-50 border-2 border-red-300 rounded-xl p-8 text-center">
                <div className="text-4xl mb-4">😔</div>
                <h3 className="text-xl font-bold text-red-800 mb-2">Failed to Load Session</h3>
                <p className="text-red-600 mb-4">{error || 'Session not found'}</p>
                <button
                    onClick={() => navigate('/history')}
                    className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                >
                    ← Back to History
                </button>
            </div>
        );
    }

    if (session.story_segments.length === 0) {
        return (
            <div className="bg-yellow-50 border-2 border-yellow-300 rounded-xl p-8 text-center">
                <div className="text-4xl mb-4">📭</div>
                <h3 className="text-xl font-bold text-yellow-800 mb-2">No Content Available</h3>
                <p className="text-yellow-600 mb-4">This session doesn't have any stored content yet.</p>
                <button
                    onClick={() => navigate('/history')}
                    className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
                >
                    ← Back to History
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            {/* Header */}
            <div className="bg-white rounded-xl p-6 shadow-md">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">{session.topic}</h1>
                        <p className="text-gray-600 mt-1">
                            Session from {new Date(session.started_at).toLocaleDateString()}
                        </p>
                    </div>
                    <button
                        onClick={() => navigate('/history')}
                        className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                    >
                        ← Back
                    </button>
                </div>

                {/* Progress */}
                <div className="mt-4">
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                        <span>Segment {currentIndex + 1} of {session.story_segments.length}</span>
                        <span>Score: ⭐ {session.score}</span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all"
                            style={{ width: `${((currentIndex + 1) / session.story_segments.length) * 100}%` }}
                        />
                    </div>
                </div>
            </div>

            {/* Scene Display */}
            {currentSegment && (
                <div className="space-y-4">
                    <SceneDisplay
                        imageUrl={currentSegment.scene_image_url ? `${BACKEND_URL}${currentSegment.scene_image_url}` : ''}
                        textOverlay={currentSegment.text_overlay}
                        isLoading={false}
                    />

                    {/* Narrative */}
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <p className="text-gray-700 leading-relaxed text-lg">
                            {currentSegment.narrative}
                        </p>
                    </div>

                    {/* Quiz Toggle */}
                    {!showQuiz ? (
                        <button
                            onClick={() => setShowQuiz(true)}
                            className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-xl font-bold hover:from-blue-600 hover:to-indigo-600"
                        >
                            📝 View Quiz Question
                        </button>
                    ) : (
                        <div className="bg-white rounded-xl p-6 shadow-lg border-2 border-indigo-200">
                            <h3 className="text-lg font-bold text-gray-800 mb-4">
                                {currentSegment.quiz.question_text}
                            </h3>

                            <div className="space-y-2 mb-4">
                                {currentSegment.quiz.options.map((opt) => {
                                    const isCorrect = currentSegment.quiz.correct_answers.includes(opt.key);
                                    return (
                                        <div
                                            key={opt.key}
                                            className={`p-3 rounded-lg border-2 ${showAnswer
                                                    ? isCorrect
                                                        ? 'border-green-500 bg-green-50'
                                                        : 'border-gray-200 bg-gray-50'
                                                    : 'border-gray-200 bg-gray-50'
                                                }`}
                                        >
                                            <span className="font-medium">{opt.key}:</span> {opt.text}
                                            {showAnswer && isCorrect && (
                                                <span className="ml-2 text-green-600">✓ Correct</span>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>

                            {!showAnswer ? (
                                <button
                                    onClick={() => setShowAnswer(true)}
                                    className="w-full py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600"
                                >
                                    Show Answer
                                </button>
                            ) : (
                                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mt-4">
                                    <p className="text-green-800 font-medium">Explanation:</p>
                                    <p className="text-green-700">{currentSegment.quiz.explanation}</p>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Navigation */}
                    <div className="flex gap-4">
                        <button
                            onClick={handlePrev}
                            disabled={currentIndex === 0}
                            className={`flex-1 py-3 rounded-xl font-bold ${currentIndex === 0
                                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                                    : 'bg-gray-600 text-white hover:bg-gray-700'
                                }`}
                        >
                            ← Previous
                        </button>
                        <button
                            onClick={handleNext}
                            disabled={currentIndex >= session.story_segments.length - 1}
                            className={`flex-1 py-3 rounded-xl font-bold ${currentIndex >= session.story_segments.length - 1
                                    ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                                    : 'bg-primary-600 text-white hover:bg-primary-700'
                                }`}
                        >
                            Next →
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};
