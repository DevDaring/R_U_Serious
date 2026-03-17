import React, { useState } from "react";
import { useLanguage } from "../contexts/LanguageContext";
import { AIIllustration, IllustrationData } from "../components/common/AIIllustration";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "";

const StoryLearning: React.FC = () => {
  const { selectedLanguage: language } = useLanguage();
  const [concept, setConcept] = useState("");
  const [story, setStory] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [studentAnswer, setStudentAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [illustration, setIllustration] = useState<IllustrationData | null>(null);
  const [storyImageUrl, setStoryImageUrl] = useState<string | null>(null);
  const [feedbackImageUrl, setFeedbackImageUrl] = useState<string | null>(null);

  const generateStory = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/story/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept, language, difficulty_level: 5 })
      });
      const data = await res.json();
      setStory(data.story);
      setFollowUp(data.follow_up_question);
      setFeedback("");
      setStudentAnswer("");
      setIllustration(data.illustration || null);
      setStoryImageUrl(data.image_url || null);
      setFeedbackImageUrl(null);
    } catch (e) {
      console.error(e);
      alert("Failed to generate story. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/story/discuss", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept, story, student_answer: studentAnswer, language })
      });
      const data = await res.json();
      setFeedback(data.response);
      setFeedbackImageUrl(data.image_url || null);
    } catch (e) {
      console.error(e);
      alert("Failed to submit answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2 text-gray-900">📖 Story Learning</h1>
        <p className="text-gray-600">
          Any concept. One story. Deep understanding.
        </p>
        <p className="text-sm text-gray-400 mt-1">
          Powered by DigitalOcean Gradient AI
        </p>
      </div>

      {!story && (
        <div className="glass-card-strong rounded-2xl p-6 border border-gray-200/50">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            What concept should the story teach?
          </label>
          <input
            className="w-full border border-gray-300 rounded-lg p-3 text-lg mb-4 bg-white text-gray-900 focus:ring-2 focus:ring-primary-500 focus:outline-none"
            placeholder="e.g., Photosynthesis, Gravity, Democracy..."
            value={concept}
            onChange={e => setConcept(e.target.value)}
          />
          <button
            onClick={generateStory}
            disabled={loading || !concept.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Crafting story..." : "Tell Me a Story"}
          </button>
        </div>
      )}

      {story && (
        <div className="space-y-6">
          {illustration && (
            <AIIllustration data={illustration} />
          )}

          {storyImageUrl && (
            <div className="flex justify-center">
              <img
                src={storyImageUrl.startsWith('data:') ? storyImageUrl : `${BACKEND_URL}${storyImageUrl}`}
                alt="Story illustration"
                className="rounded-xl border-2 border-amber-200 shadow-md max-h-64 object-contain"
                onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
              />
            </div>
          )}
          
          <div className="bg-amber-50/80 border-l-4 border-amber-400 p-5 rounded-2xl backdrop-blur-sm">
            <h2 className="text-sm font-semibold text-amber-800 mb-2">📚 The Story</h2>
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{story}</p>
          </div>

          <div className="bg-blue-50/80 border border-blue-200/50 p-4 rounded-2xl backdrop-blur-sm">
            <p className="font-semibold text-blue-800">🤔 {followUp}</p>
          </div>

          {!feedback && (
            <div className="glass-card-strong rounded-2xl p-4">
              <textarea
                className="w-full border border-gray-300 rounded-lg p-3 mb-3 bg-white text-gray-900 focus:ring-2 focus:ring-green-500 focus:outline-none"
                rows={3}
                placeholder="Your answer..."
                value={studentAnswer}
                onChange={e => setStudentAnswer(e.target.value)}
              />
              <button
                onClick={submitAnswer}
                disabled={loading || !studentAnswer.trim()}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? "Thinking..." : "Submit Answer"}
              </button>
            </div>
          )}

          {feedback && (
            <div className="bg-green-50/80 border border-green-200/50 p-4 rounded-2xl backdrop-blur-sm">
              <h3 className="text-sm font-semibold text-green-800 mb-2">💡 Feedback</h3>
              <p className="text-gray-800 whitespace-pre-wrap">{feedback}</p>
              {feedbackImageUrl && (
                <div className="flex justify-center mt-3">
                  <img
                    src={feedbackImageUrl.startsWith('data:') ? feedbackImageUrl : `${BACKEND_URL}${feedbackImageUrl}`}
                    alt="Feedback illustration"
                    className="rounded-xl border-2 border-green-200 shadow-md max-h-64 object-contain"
                    onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
                  />
                </div>
              )}
            </div>
          )}

          <button
            onClick={() => { setStory(""); setFollowUp(""); setFeedback(""); setConcept(""); setIllustration(null); setStoryImageUrl(null); setFeedbackImageUrl(null); }}
            className="text-blue-600 hover:text-blue-700 underline text-sm"
          >
            Try another concept
          </button>
        </div>
      )}
    </div>
  );
};

export default StoryLearning;
