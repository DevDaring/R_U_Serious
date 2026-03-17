import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { cn } from '../../utils/helpers';

interface MenuItem {
  path: string;
  label: string;
  icon: string;
  adminOnly?: boolean;
}

const menuItems: MenuItem[] = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/learning', label: 'Start Learning', icon: '📚' },
  // Core Learning Features
  { path: '/story-learning', label: 'Story Learning', icon: '📖' },
  { path: '/feynman', label: 'Feynman Technique', icon: '🧠' },
  { path: '/mistake-autopsy', label: 'MCT Diagnose', icon: '🔬' },
  // User Features
  { path: '/history', label: 'History', icon: '📜' },
  { path: '/profile', label: 'Profile', icon: '⚙️' },
  { path: '/admin', label: 'Admin Panel', icon: '🔧', adminOnly: true },
];

export const LeftMenu: React.FC = () => {
  const location = useLocation();
  const { isAdmin } = useAuth();
  const [isExpanded, setIsExpanded] = useState(false);

  const filteredItems = menuItems.filter(item => !item.adminOnly || isAdmin);

  return (
    <aside
      className={cn(
        'bg-white border-r border-gray-200 h-full overflow-y-auto transition-all duration-300 ease-in-out relative z-50',
        isExpanded ? 'w-64' : 'w-16'
      )}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
    >
      <nav className={cn(
        'space-y-2',
        isExpanded ? 'p-4' : 'px-2 py-4'
      )}>
        {filteredItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={cn(
              'flex items-center rounded-lg transition-all duration-200',
              isExpanded ? 'space-x-3 px-4 py-3' : 'justify-center px-2 py-3',
              location.pathname.startsWith(item.path)
                ? 'bg-primary-100 text-primary-700 font-semibold'
                : 'text-gray-700 hover:bg-gray-100'
            )}
            title={item.label}
          >
            <span className={cn(
              'flex-shrink-0',
              isExpanded ? 'text-2xl' : 'text-xl'
            )}>
              {item.icon}
            </span>
            {isExpanded && (
              <span className="whitespace-nowrap opacity-0 animate-fadeIn">
                {item.label}
              </span>
            )}
          </Link>
        ))}
      </nav>

      {/* Custom inline styles for the fade-in animation */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateX(-10px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.2s ease-out forwards;
        }
      `}</style>
    </aside>
  );
};
