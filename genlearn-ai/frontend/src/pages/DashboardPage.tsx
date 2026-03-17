import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/common/Button';
import { ProgressBar } from '../components/common/ProgressBar';
import { xpForNextLevel } from '../utils/helpers';
import { PageTransition, FadeIn, ScaleIn } from '../components/effects/PageTransition';

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <PageTransition>
    <div className="space-y-6">
      <FadeIn>
      <div className="bg-gradient-to-r from-primary-600 via-primary-500 to-indigo-600 rounded-2xl p-8 text-white flex items-center gap-6 shadow-lg relative overflow-hidden">
        {/* Decorative circles */}
        <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/4" />
        <div className="absolute bottom-0 left-1/4 w-24 h-24 bg-white/5 rounded-full translate-y-1/2" />
        <img
          src="/assets/site-images/ritty.png"
          alt="Ritty"
          className="w-20 h-20 rounded-full border-3 border-white/30 shadow-lg object-cover hidden md:block relative z-10"
        />
        <div className="relative z-10">
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user.display_name}!</h1>
          <p className="text-primary-100">Ready to continue your learning journey?</p>
        </div>
      </div>
      </FadeIn>

      <div className="grid md:grid-cols-3 gap-6">
        {[
          { title: 'Level', value: user.level, color: 'text-primary-600', accent: 'from-primary-400 to-primary-600', hasProgress: true },
          { title: 'Total XP', value: user.xp_points, color: 'text-yellow-600', accent: 'from-yellow-400 to-orange-500', subtitle: 'Keep learning to earn more XP!' },
          { title: 'Streak', value: user.streak_days, color: 'text-orange-600', accent: 'from-orange-400 to-red-500', subtitle: 'Days of consecutive learning' },
        ].map((stat, i) => (
          <ScaleIn key={i} delay={0.1 * i}>
            <div className="glass-card rounded-2xl p-6 hover-lift relative overflow-hidden">
              <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${stat.accent}`} />
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-700">{stat.title}</h3>
                <span className={`text-3xl font-bold ${stat.color}`}>{stat.value}</span>
              </div>
              {stat.hasProgress ? (
                <>
                  <ProgressBar value={user.xp_points % 500} max={500} label="XP Progress" color="primary" />
                  <p className="text-sm text-gray-500 mt-2">{xpForNextLevel(user.xp_points)} XP to next level</p>
                </>
              ) : (
                <p className="text-gray-500">{stat.subtitle}</p>
              )}
            </div>
          </ScaleIn>
        ))}
      </div>

      <FadeIn delay={0.3}>
      <div className="glass-card-strong rounded-2xl p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Quick Actions</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link to="/learning">
            <Button variant="primary" size="lg" className="w-full shadow-md hover:shadow-lg transition-shadow">
              📚 Start Learning
            </Button>
          </Link>
          <Link to="/story-learning">
            <Button variant="secondary" size="lg" className="w-full hover:shadow-md transition-shadow">
              📖 Story Learning
            </Button>
          </Link>
          <Link to="/feynman">
            <Button variant="secondary" size="lg" className="w-full hover:shadow-md transition-shadow">
              🧠 Feynman Technique
            </Button>
          </Link>
          <Link to="/mistake-autopsy">
            <Button variant="secondary" size="lg" className="w-full hover:shadow-md transition-shadow">
              🔬 Mistake Autopsy
            </Button>
          </Link>
        </div>
      </div>
      </FadeIn>

      <FadeIn delay={0.4}>
      <div className="glass-card rounded-2xl p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Recent Activity</h2>
        <div className="text-center text-gray-500 py-8">
          <div className="text-4xl mb-3">📝</div>
          <p>No recent activity yet.</p>
          <p className="text-sm mt-2">Start a learning session to see your activity here!</p>
        </div>
      </div>
      </FadeIn>
    </div>
    </PageTransition>
  );
};
