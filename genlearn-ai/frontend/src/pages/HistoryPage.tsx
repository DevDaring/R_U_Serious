import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface SessionHistory {
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
}

interface HistoryResponse {
  sessions: SessionHistory[];
  total: number;
  limit: number;
  offset: number;
}

export const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState<SessionHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const response: HistoryResponse = await api.getSessionHistory(20, 0);
      setSessions(response.sessions || []);
      setTotal(response.total || 0);
    } catch (err: any) {
      console.error('Failed to load history:', err);
      setError(err.response?.data?.detail || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'N/A';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateStr;
    }
  };

  const getStatusBadge = (status: string) => {
    const badges: Record<string, { bg: string; text: string; label: string }> = {
      completed: { bg: 'bg-green-100', text: 'text-green-800', label: '✅ Completed' },
      in_progress: { bg: 'bg-yellow-100', text: 'text-yellow-800', label: '⏳ In Progress' },
      unknown: { bg: 'bg-gray-100', text: 'text-gray-800', label: '❓ Unknown' }
    };
    const badge = badges[status] || badges.unknown;
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${badge.bg} ${badge.text}`}>
        {badge.label}
      </span>
    );
  };

  const getStyleEmoji = (style: string) => {
    const emojis: Record<string, string> = {
      thriller: '🔪',
      fun: '🎉',
      nostalgic: '📻',
      adventure: '🗺️',
      mystery: '🔍',
      scifi: '🚀'
    };
    return emojis[style] || '📖';
  };

  const handleRevision = (sessionId: string) => {
    navigate(`/learning/revision/${sessionId}`);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mb-4"></div>
        <p className="text-gray-600">Loading your learning history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-xl p-8 text-center">
        <div className="text-4xl mb-4">😔</div>
        <h3 className="text-xl font-bold text-red-800 mb-2">Failed to Load History</h3>
        <p className="text-red-600 mb-4">{error}</p>
        <button
          onClick={loadHistory}
          className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-6 shadow-md">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">📜 Learning History</h1>
            <p className="text-gray-600 mt-1">
              {total} session{total !== 1 ? 's' : ''} total • Review and revise your past learning
            </p>
          </div>
          <button
            onClick={() => navigate('/learning')}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium"
          >
            ➕ New Session
          </button>
        </div>

        {sessions.length === 0 ? (
          <div className="text-center py-16 text-gray-600">
            <div className="text-6xl mb-4">📚</div>
            <p className="text-lg">No learning sessions yet.</p>
            <p className="text-sm mt-2">Start your first learning adventure!</p>
            <button
              onClick={() => navigate('/learning')}
              className="mt-6 px-6 py-3 bg-gradient-to-r from-primary-500 to-purple-500 text-white rounded-lg hover:from-primary-600 hover:to-purple-600 font-medium"
            >
              🚀 Start Learning
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {sessions.map((session) => (
              <div
                key={session.session_id}
                className="border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow bg-gradient-to-r from-white to-gray-50"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-2xl">{getStyleEmoji(session.story_style)}</span>
                      <h3 className="text-xl font-bold text-gray-900">{session.topic}</h3>
                      {getStatusBadge(session.status)}
                    </div>

                    <div className="flex flex-wrap gap-4 text-sm text-gray-600 mt-3">
                      <span className="flex items-center gap-1">
                        📊 Difficulty: {session.difficulty_level}/10
                      </span>
                      <span className="flex items-center gap-1">
                        ⏱️ {session.duration_minutes} min
                      </span>
                      <span className="flex items-center gap-1">
                        ⭐ Score: {session.score}
                      </span>
                      <span className="flex items-center gap-1">
                        🎨 {session.visual_style}
                      </span>
                    </div>

                    <div className="text-xs text-gray-500 mt-3">
                      Started: {formatDate(session.started_at)}
                      {session.completed_at && ` • Completed: ${formatDate(session.completed_at)}`}
                    </div>
                  </div>

                  <div className="flex gap-2 ml-4">
                    <button
                      onClick={() => handleRevision(session.session_id)}
                      className="px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg hover:from-blue-600 hover:to-indigo-600 font-medium text-sm"
                    >
                      📖 Review
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
