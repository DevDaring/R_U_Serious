import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { APP_NAME } from '../utils/constants';
import { Button } from '../components/common/Button';

export const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Hero Section with Background Image */}
      <div
        className="relative min-h-[80vh] flex items-center justify-center bg-cover bg-center"
        style={{ backgroundImage: "url('/assets/site-images/hero-bg.png')" }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-primary-700/85 to-primary-900/85" />
        <div className="relative z-10 container mx-auto px-4 text-center">
          <div className="flex justify-center mb-6">
            <img
              src="/assets/site-images/ritty.png"
              alt="Ritty - AI Learning Companion"
              className="w-28 h-28 rounded-full border-4 border-white/30 shadow-2xl object-cover"
            />
          </div>
          <h1 className="text-6xl font-extrabold text-white mb-4 drop-shadow-lg">
            {APP_NAME}
          </h1>
          <p className="text-2xl text-white/90 mb-3 max-w-2xl mx-auto">
            Generative AI-Powered Adaptive Learning
          </p>
          <p className="text-lg text-white/70 mb-8 max-w-xl mx-auto">
            Learn anything through stories, the Feynman Technique, and AI-guided mistake analysis
          </p>
          <div className="flex justify-center space-x-4">
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button size="lg" variant="secondary">
                  Go to Dashboard
                </Button>
              </Link>
            ) : (
              <Link to="/login">
                <button className="px-8 py-4 bg-white text-primary-700 font-bold text-lg rounded-xl hover:bg-gray-100 shadow-xl transition-all hover:scale-105">
                  Get Started Free
                </button>
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">How It Works</h2>
          <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
            Three powerful AI-driven learning methods to help you truly understand any concept
          </p>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                icon: '📖',
                title: 'Story Learning',
                desc: 'Turn any concept into an engaging story with AI-generated narratives and follow-up discussions',
                color: 'from-blue-500 to-cyan-500'
              },
              {
                icon: '🧠',
                title: 'Feynman Technique',
                desc: '5 layers of mastery: teach Ritty, compress, spiral deep, build analogies, face the lecture hall',
                color: 'from-purple-500 to-pink-500'
              },
              {
                icon: '🔬',
                title: 'Mistake Autopsy',
                desc: 'Trace your mistakes to their root cause with AI-powered misconception cascade tracing',
                color: 'from-teal-500 to-green-500'
              },
            ].map((feature, i) => (
              <div key={i} className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
                <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-3xl mb-5 shadow-md`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Powered By Section */}
      <div className="bg-white py-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm uppercase tracking-wider text-gray-500 mb-4">Powered by</p>
          <div className="flex justify-center items-center gap-8 flex-wrap">
            <div className="flex items-center gap-2 px-6 py-3 bg-gray-50 rounded-lg">
              <span className="text-2xl">🤖</span>
              <span className="font-semibold text-gray-700">DigitalOcean Gradient AI</span>
            </div>
            <div className="flex items-center gap-2 px-6 py-3 bg-gray-50 rounded-lg">
              <span className="text-2xl">☁️</span>
              <span className="font-semibold text-gray-700">DigitalOcean Cloud</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-900 py-8 text-center">
        <p className="text-gray-400 text-sm">
          Built for the DigitalOcean GenAI Hackathon 2025
        </p>
      </div>
    </div>
  );
};
