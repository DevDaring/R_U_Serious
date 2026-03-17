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
    </main>
  );
};
