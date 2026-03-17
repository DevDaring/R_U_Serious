import React, { useState } from 'react';
import { ChatWindow } from '../chat/ChatWindow';

export const RightPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <aside
      className={cn(
        'bg-white border-l border-gray-200 h-full transition-all duration-300',
        isOpen ? 'w-80' : 'w-0 overflow-hidden'
      )}
    >
      <div className="relative h-full">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="absolute -left-8 top-4 bg-primary-600 text-white p-2 rounded-l-lg shadow-lg hover:bg-primary-700 transition-colors"
        >
          {isOpen ? '→' : '←'}
        </button>

        {isOpen && (
          <div className="h-full flex flex-col">
            <div className="p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">AI Assistant</h3>
              <p className="text-sm text-gray-600">Ask me anything!</p>
            </div>
            <ChatWindow />
          </div>
        )}
      </div>
    </aside>
  );
};

function cn(...classes: (string | boolean)[]) {
  return classes.filter(Boolean).join(' ');
}
