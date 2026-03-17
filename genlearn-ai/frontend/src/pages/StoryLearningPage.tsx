import React, { useState } from "react";
import { useLanguage } from "../contexts/LanguageContext";

const StoryLearning: React.FC = () => {
  const { language } = useLanguage();
  const [concept, setConcept] = useState("");
  const [story, setStory] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [studentAnswer, setStudentAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

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
        <p className="text-sm text-gray-500 mt-1">
          Powered by DigitalOcean Gradient AI
        </p>
      </div>

      {!story && (
        <div className="bg-white rounded-lg p-6 shadow-md border border-gray-200">
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
          <div className="bg-amber-50 border-l-4 border-amber-400 p-5 rounded-lg">
            <h2 className="text-sm font-semibold text-amber-800 mb-2">📚 The Story</h2>
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{story}</p>
          </div>

          <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
            <p className="font-semibold text-blue-800">🤔 {followUp}</p>
          </div>

          {!feedback && (
            <div className="bg-white rounded-lg p-4 shadow-md border border-gray-200">
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
            <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
              <h3 className="text-sm font-semibold text-green-800 mb-2">💡 Feedback</h3>
              <p className="text-gray-800 whitespace-pre-wrap">{feedback}</p>
            </div>
          )}

          <button
            onClick={() => { setStory(""); setFollowUp(""); setFeedback(""); setConcept(""); }}
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
