import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { APP_NAME } from '../../utils/constants';
import { useLanguage } from '../../contexts/LanguageContext';
import { SUPPORTED_LANGUAGES } from '../../constants/languages';

export const TopNavbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { selectedLanguage, setLanguage } = useLanguage();

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value);
  };

  return (
    <nav className="glass-navbar">
      <div className="px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">G</span>
          </div>
          <span className="text-2xl font-bold text-gray-900">{APP_NAME}</span>
        </Link>

        {/* Powered by DO badge */}
        <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-full">
          <svg className="w-4 h-4 text-blue-600" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 5.46 4.45 9.91 9.91 9.91v-3.57c-3.57 0-6.34-2.77-6.34-6.34s2.77-6.34 6.34-6.34 6.34 2.77 6.34 6.34h3.57C21.95 6.45 17.5 2 12.04 2z"/></svg>
          <span className="text-xs font-semibold text-blue-700">Powered by DO Gradient AI</span>
        </div>

        <div className="flex items-center space-x-6">
          {user && (
            <>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Level {user.level}</span>
                <div className="w-32 h-2 bg-gray-200 rounded-full">
                  <div
                    className="h-2 bg-primary-600 rounded-full transition-all"
                    style={{ width: `${(user.xp_points % 500) / 5}%` }}
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span className="text-sm font-semibold text-gray-900">{user.xp_points} XP</span>
              </div>

              {/* Language Selector */}
              <div className="flex items-center space-x-2">
                <span className="text-lg">🌐</span>
                <select
                  value={selectedLanguage}
                  onChange={handleLanguageChange}
                  className="px-2 py-1 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white cursor-pointer"
                >
                  {SUPPORTED_LANGUAGES.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.nativeName}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center space-x-3">
                <span className="text-sm font-medium text-gray-700">{user.display_name}</span>
                <button
                  onClick={logout}
                  className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
                >
                  Logout
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};
