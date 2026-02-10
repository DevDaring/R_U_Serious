import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../common/Button';
import { APP_NAME } from '../../utils/constants';

export const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('DebK');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl flex overflow-hidden">
        {/* Left: Feynman Image */}
        <div className="hidden md:flex md:w-1/2 bg-gradient-to-b from-primary-600 to-primary-800 flex-col items-center justify-center p-8 relative">
          <img
            src="/assets/site-images/richard.png"
            alt="Richard Feynman"
            className="w-72 object-contain rounded-xl border-4 border-white/30 shadow-xl mb-6"
          />
          <h2 className="text-white text-xl font-bold text-center">"If you can't explain it simply, you don't understand it well enough."</h2>
          <p className="text-primary-200 mt-3 text-sm font-medium">— Richard Feynman</p>
          <div className="absolute bottom-4 text-primary-300 text-xs">Powered by Gemini 3</div>
        </div>

        {/* Right: Login Form */}
        <div className="w-full md:w-1/2 p-8">
        <div className="text-center mb-8">
          {/* Show Feynman image on mobile too */}
          <img
            src="/assets/site-images/richard.png"
            alt="Richard Feynman"
            className="md:hidden mx-auto mb-4 w-24 object-contain rounded-xl border-2 border-primary-300 shadow-lg"
          />
          <h1 className="text-2xl font-bold text-gray-900">{APP_NAME}</h1>
          <p className="text-sm text-gray-500">Learn with the Feynman Technique</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border-2 border-red-300 text-red-800 px-4 py-3 rounded-lg font-medium">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-gray-900 placeholder-gray-500 font-medium selection:bg-primary-200 selection:text-gray-900"
              placeholder="Enter your username"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-gray-900 placeholder-gray-500 font-medium selection:bg-primary-200 selection:text-gray-900"
              placeholder="Enter your password"
              required
            />
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={isLoading}
            className="w-full"
          >
            Sign In
          </Button>
        </form>

        <div className="mt-6 text-center text-sm">
          <p className="text-gray-600 mb-2">Demo credentials:</p>
          <p className="font-mono text-gray-800 font-medium">DebK / password123</p>
        </div>
      </div>
      </div>
    </div>
  );
};
