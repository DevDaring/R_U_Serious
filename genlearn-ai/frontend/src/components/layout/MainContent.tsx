import React from 'react';
import { AmbientParticles } from '../effects/AmbientParticles';

interface MainContentProps {
  children: React.ReactNode;
}

export const MainContent: React.FC<MainContentProps> = ({ children }) => {
  return (
    <main className="flex-1 overflow-y-auto bg-gradient-to-br from-gray-50 via-white to-blue-50/30 relative">
      <AmbientParticles theme="sunny" className="opacity-40" />
      <div className="container mx-auto p-6 relative z-10">
        {children}
      </div>
      <div className="relative z-10 py-3 text-center border-t border-gray-200/50">
        <div className="flex justify-center items-center gap-1.5">
          <svg className="w-3.5 h-3.5 text-blue-500" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 5.46 4.45 9.91 9.91 9.91v-3.57c-3.57 0-6.34-2.77-6.34-6.34s2.77-6.34 6.34-6.34 6.34 2.77 6.34 6.34h3.57C21.95 6.45 17.5 2 12.04 2z"/></svg>
          <span className="text-xs text-gray-400">Powered by DigitalOcean Gradient™ AI</span>
        </div>
      </div>
    </main>
  );
};
