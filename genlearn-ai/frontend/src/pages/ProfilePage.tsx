import React from 'react';
import { useAuth } from '../hooks/useAuth';

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg p-8 shadow-md">
        <h1 className="text-3xl font-bold mb-6">Profile Settings</h1>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Display Name</label>
            <input
              type="text"
              value={user.display_name}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              readOnly
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={user.email}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              readOnly
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
            <input
              type="text"
              value={user.language_preference}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              readOnly
            />
          </div>
        </div>

        <div className="mt-6 text-sm text-gray-600">
          Profile editing features will be available soon.
        </div>
      </div>
    </div>
  );
};
