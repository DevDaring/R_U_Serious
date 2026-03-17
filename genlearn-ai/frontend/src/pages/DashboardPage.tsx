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
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-8 text-white flex items-center gap-6">
        <img
          src="/assets/site-images/ritty.png"
          alt="Ritty"
          className="w-20 h-20 rounded-full border-3 border-white/30 shadow-lg object-cover hidden md:block"
        />
        <div>
          <h1 className="text-3xl font-bold mb-2">Welcome back, {user.display_name}!</h1>
          <p className="text-primary-100">Ready to continue your learning journey?</p>
        </div>
      </div>
      </FadeIn>

      <div className="grid md:grid-cols-3 gap-6">
        {[
          { title: 'Level', value: user.level, color: 'text-primary-600', hasProgress: true },
          { title: 'Total XP', value: user.xp_points, color: 'text-yellow-600', subtitle: 'Keep learning to earn more XP!' },
          { title: 'Streak', value: user.streak_days, color: 'text-orange-600', subtitle: 'Days of consecutive learning' },
        ].map((stat, i) => (
          <ScaleIn key={i} delay={0.1 * i}>
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">{stat.title}</h3>
                <span className={`text-3xl font-bold ${stat.color}`}>{stat.value}</span>
              </div>
              {stat.hasProgress ? (
                <>
                  <ProgressBar value={user.xp_points % 500} max={500} label="XP Progress" color="primary" />
                  <p className="text-sm text-gray-600 mt-2">{xpForNextLevel(user.xp_points)} XP to next level</p>
                </>
              ) : (
                <p className="text-gray-600">{stat.subtitle}</p>
              )}
            </div>
          </ScaleIn>
        ))}
      </div>

      <FadeIn delay={0.3}>
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link to="/learning">
            <Button variant="primary" size="lg" className="w-full">
              📚 Start Learning
            </Button>
          </Link>
          <Link to="/story-learning">
            <Button variant="secondary" size="lg" className="w-full">
              📖 Story Learning
            </Button>
          </Link>
          <Link to="/feynman">
            <Button variant="secondary" size="lg" className="w-full">
              🧠 Feynman Technique
            </Button>
          </Link>
          <Link to="/mistake-autopsy">
            <Button variant="secondary" size="lg" className="w-full">
              🔬 Mistake Autopsy
            </Button>
          </Link>
        </div>
      </div>
      </FadeIn>

      <FadeIn delay={0.4}>
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h2 className="text-2xl font-bold mb-6">Recent Activity</h2>
        <div className="text-center text-gray-600 py-8">
          <p>No recent activity yet.</p>
          <p className="text-sm mt-2">Start a learning session to see your activity here!</p>
        </div>
      </div>
      </FadeIn>
    </div>
    </PageTransition>
  );
};
