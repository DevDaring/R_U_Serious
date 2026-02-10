import React, { useState, useEffect } from 'react';
import { SceneDisplay } from './SceneDisplay';
import { QuizCard, QuizResult } from './QuizCard';
import { ResultsSummary } from './ResultsSummary';
import { LearningSession } from '../../types';
import api, { BACKEND_URL } from '../../services/api';

interface TextOverlay {
    text: string;
    position: 'top' | 'center' | 'bottom';
    style: 'speech_bubble' | 'caption' | 'dramatic';
}

interface QuizOption {
    key: string;
    text: string;
    is_correct: boolean;
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
    audio_url?: string;
    quiz: Quiz;
}

interface StoryPlayerProps {
    session: LearningSession;
    onComplete: (results: SessionResults) => void;
}

interface SessionResults {
    totalScore: number;
    correctAnswers: number;
    totalQuestions: number;
    xpEarned: number;
    timeSpent: number;
    longestStreak: number;
}

type Phase = 'loading' | 'story' | 'quiz' | 'result' | 'complete';

export const StoryPlayer: React.FC<StoryPlayerProps> = ({ session, onComplete }) => {
    const [segments, setSegments] = useState<StorySegment[]>([]);
    const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0);
    const [phase, setPhase] = useState<Phase>('loading');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Scoring
    const [score, setScore] = useState(0);
    const [correctAnswers, setCorrectAnswers] = useState(0);
    const [currentStreak, setCurrentStreak] = useState(0);
    const [longestStreak, setLongestStreak] = useState(0);
    const [startTime] = useState(Date.now());

    // Quiz result state
    const [lastAnswerCorrect, setLastAnswerCorrect] = useState(false);
    const [lastExplanation, setLastExplanation] = useState('');
    const [lastCorrectAnswer, setLastCorrectAnswer] = useState('');
    const [lastPointsEarned, setLastPointsEarned] = useState(0);

    useEffect(() => {
        loadContent();
    }, [session.session_id]);

    const loadContent = async () => {
        try {
            setIsLoading(true);
            setError(null);

            // Fetch enhanced content from backend
            const response = await api.get(`/learning/session/${session.session_id}/content`);

            // Process segments from backend (enhanced format)
            const enhancedSegments = processSegments(
                response.data.story_segments || [],
                session.topic,
                session.total_cycles
            );

            setSegments(enhancedSegments);
            setPhase('story');
        } catch (err: any) {
            console.error('Failed to load content:', err);
            setError(err.response?.data?.detail || 'Failed to load learning content');
        } finally {
            setIsLoading(false);
        }
    };

    // Process segments from backend (now returns enhanced format)
    const processSegments = (
        backendSegments: any[],
        topic: string,
        numSegments: number
    ): StorySegment[] => {
        // If we have segments from backend, use them directly (enhanced format)
        if (backendSegments.length > 0) {
            return backendSegments.map((seg, idx) => ({
                segment_number: seg.segment_number || idx + 1,
                narrative: seg.narrative || `Learning about ${topic}...`,
                scene_description: seg.scene_description || seg.image_prompt || `Scene about ${topic}`,
                scene_image_url: seg.scene_image_url || seg.image_url || '',
                text_overlay: seg.text_overlay || {
                    text: seg.narrative?.substring(0, 80) || `Let's explore ${topic}!`,
                    position: 'bottom' as const,
                    style: 'caption' as const
                },
                audio_url: seg.audio_url,
                quiz: seg.quiz ? {
                    question_id: seg.quiz.question_id || `Q${idx + 1}`,
                    question_text: seg.quiz.question_text || `What did you learn about ${topic}?`,
                    options: seg.quiz.options || [
                        { key: 'A', text: 'Option A', is_correct: false },
                        { key: 'B', text: 'Option B', is_correct: false },
                        { key: 'C', text: 'Option C', is_correct: false },
                        { key: 'D', text: 'Option D', is_correct: false }
                    ],
                    correct_answers: seg.quiz.correct_answers || ['A'],
                    explanation: seg.quiz.explanation || 'This is the explanation.',
                    is_multi_select: seg.quiz.is_multi_select || false,
                    points: seg.quiz.points || 10
                } : generateMockQuiz(idx + 1, topic)
            }));
        }

        // Generate mock segments if none from backend
        return Array.from({ length: numSegments }, (_, idx) => ({
            segment_number: idx + 1,
            narrative: `Segment ${idx + 1} of our ${topic} adventure...`,
            scene_description: `A scene depicting ${topic}`,
            scene_image_url: '',
            text_overlay: {
                text: `Chapter ${idx + 1}: Exploring ${topic}`,
                position: 'bottom' as const,
                style: 'caption' as const
            },
            quiz: generateMockQuiz(idx + 1, topic)
        }));
    };

    const generateMockQuiz = (segmentNum: number, topic: string): Quiz => ({
        question_id: `Q${segmentNum}`,
        question_text: `What did you learn about ${topic} in this segment?`,
        options: [
            { key: 'A', text: 'The first concept we explored', is_correct: true },
            { key: 'B', text: 'Something unrelated', is_correct: false },
            { key: 'C', text: 'A different topic entirely', is_correct: false },
            { key: 'D', text: 'None of the above', is_correct: false }
        ],
        correct_answers: ['A'],
        explanation: `In this segment, we learned important concepts about ${topic}. The key takeaway was understanding the fundamentals.`,
        is_multi_select: false,
        points: 10
    });

    const currentSegment = segments[currentSegmentIndex];

    const handleContinueToQuiz = () => {
        setPhase('quiz');
    };

    const handleQuizAnswer = (selectedKeys: string[]) => {
        if (!currentSegment) return;

        const quiz = currentSegment.quiz;
        const isCorrect = selectedKeys.sort().join(',') === quiz.correct_answers.sort().join(',');

        // Calculate points
        let pointsEarned = isCorrect ? quiz.points : 2; // Participation points

        // Streak bonus
        const newStreak = isCorrect ? currentStreak + 1 : 0;
        if (newStreak >= 3) {
            pointsEarned += 5; // Streak bonus
        }

        setScore(prev => prev + pointsEarned);
        if (isCorrect) {
            setCorrectAnswers(prev => prev + 1);
        }
        setCurrentStreak(newStreak);
        setLongestStreak(prev => Math.max(prev, newStreak));

        // Store result for display
        setLastAnswerCorrect(isCorrect);
        setLastPointsEarned(pointsEarned);
        setLastExplanation(quiz.explanation);
        setLastCorrectAnswer(
            quiz.options
                .filter(o => quiz.correct_answers.includes(o.key))
                .map(o => `${o.key}: ${o.text}`)
                .join(', ')
        );

        setPhase('result');
    };

    const handleContinueAfterResult = () => {
        if (currentSegmentIndex < segments.length - 1) {
            setCurrentSegmentIndex(prev => prev + 1);
            setPhase('story');
        } else {
            // Session complete
            const timeSpent = Math.floor((Date.now() - startTime) / 1000);
            const xpEarned = score * (session.difficulty_level || 1);

            onComplete({
                totalScore: score,
                correctAnswers,
                totalQuestions: segments.length,
                xpEarned,
                timeSpent,
                longestStreak
            });

            setPhase('complete');
        }
    };

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <div className="animate-spin w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full mb-4"></div>
                <p className="text-xl text-gray-600">Generating your learning adventure...</p>
                <p className="text-gray-500 mt-2">Creating scenes and questions for {session.topic}</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border-2 border-red-300 rounded-xl p-8 text-center">
                <div className="text-4xl mb-4">😔</div>
                <h3 className="text-xl font-bold text-red-800 mb-2">Oops! Something went wrong</h3>
                <p className="text-red-600 mb-4">{error}</p>
                <button
                    onClick={loadContent}
                    className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                    Try Again
                </button>
            </div>
        );
    }

    if (phase === 'complete') {
        return (
            <ResultsSummary
                topic={session.topic}
                totalQuestions={segments.length}
                correctAnswers={correctAnswers}
                totalScore={score}
                xpEarned={score * (session.difficulty_level || 1)}
                timeSpent={Math.floor((Date.now() - startTime) / 1000)}
                longestStreak={longestStreak}
                onPlayAgain={() => window.location.reload()}
                onGoHome={() => window.location.href = '/'}
            />
        );
    }

    if (!currentSegment) {
        return <div>No content available</div>;
    }

    return (
        <div className="max-w-2xl mx-auto">
            {/* Progress Bar */}
            <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-600">
                        Progress: {currentSegmentIndex + 1}/{segments.length}
                    </span>
                    <span className="text-sm font-medium text-yellow-600">
                        ⭐ {score} points
                    </span>
                </div>
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all duration-500"
                        style={{ width: `${((currentSegmentIndex + 1) / segments.length) * 100}%` }}
                    />
                </div>
            </div>

            {/* Story Phase */}
            {phase === 'story' && (
                <div className="space-y-6">
                    <SceneDisplay
                        imageUrl={currentSegment.scene_image_url ? `${BACKEND_URL}${currentSegment.scene_image_url}` : ''}
                        textOverlay={currentSegment.text_overlay}
                        isLoading={!currentSegment.scene_image_url}
                    />

                    {/* Narrative */}
                    <div className="bg-white rounded-xl p-6 shadow-lg">
                        <p className="text-gray-700 leading-relaxed text-lg">
                            {currentSegment.narrative}
                        </p>
                    </div>

                    <button
                        onClick={handleContinueToQuiz}
                        className="w-full py-4 rounded-xl font-bold text-lg bg-gradient-to-r from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 shadow-lg transition-all"
                    >
                        📝 Take the Quiz →
                    </button>
                </div>
            )}

            {/* Quiz Phase */}
            {phase === 'quiz' && (
                <QuizCard
                    questionNumber={currentSegmentIndex + 1}
                    totalQuestions={segments.length}
                    questionText={currentSegment.quiz.question_text}
                    options={currentSegment.quiz.options.map(o => ({ key: o.key, text: o.text }))}
                    isMultiSelect={currentSegment.quiz.is_multi_select}
                    points={currentSegment.quiz.points}
                    onAnswer={handleQuizAnswer}
                />
            )}

            {/* Result Phase */}
            {phase === 'result' && (
                <QuizResult
                    isCorrect={lastAnswerCorrect}
                    correctAnswer={lastCorrectAnswer}
                    explanation={lastExplanation}
                    pointsEarned={lastPointsEarned}
                    streak={currentStreak}
                    onContinue={handleContinueAfterResult}
                />
            )}
        </div>
    );
};
