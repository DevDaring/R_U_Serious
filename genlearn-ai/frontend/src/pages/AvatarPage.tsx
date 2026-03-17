import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AvatarCreator } from '../components/avatar/AvatarCreator';

export const AvatarPage: React.FC = () => {
  const navigate = useNavigate();
  const [created, setCreated] = useState<any>(null);

  const handleComplete = (avatar: any) => {
    setCreated(avatar);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Create Your Avatar</h1>
        <p className="text-gray-600 mt-1">Draw, upload, or pick from the gallery</p>
      </div>

      {created ? (
        <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
          <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden border-4 border-primary-200">
            <img src={created.image_url} alt={created.name || 'Avatar'} className="w-full h-full object-cover" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Avatar Created!</h2>
          <p className="text-gray-600 mb-6">{created.name || 'Your new avatar is ready'}</p>
          <div className="flex justify-center gap-4">
            <button
              onClick={() => setCreated(null)}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Create Another
            </button>
            <button
              onClick={() => navigate('/learning')}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              Start Learning
            </button>
          </div>
        </div>
      ) : (
        <AvatarCreator
          onComplete={handleComplete}
          onCancel={() => navigate(-1)}
        />
      )}
    </div>
  );
};
