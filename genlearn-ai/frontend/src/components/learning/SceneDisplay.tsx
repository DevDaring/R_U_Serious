import React from 'react';

interface TextOverlayData {
    text: string;
    position: 'top' | 'center' | 'bottom';
    style: 'speech_bubble' | 'caption' | 'dramatic';
}

interface SceneDisplayProps {
    imageUrl: string;
    textOverlay: TextOverlayData;
    isLoading?: boolean;
}

export const SceneDisplay: React.FC<SceneDisplayProps> = ({
    imageUrl,
    textOverlay,
    isLoading = false
}) => {
    const getPositionClass = (position: string): string => {
        switch (position) {
            case 'top':
                return 'top-4 left-0 right-0';
            case 'center':
                return 'top-1/2 left-0 right-0 -translate-y-1/2';
            case 'bottom':
            default:
                return 'bottom-4 left-0 right-0';
        }
    };

    const getStyleClass = (style: string): string => {
        switch (style) {
            case 'speech_bubble':
                return 'mx-4 bg-white rounded-2xl p-4 shadow-lg border-2 border-gray-200 relative before:content-[""] before:absolute before:bottom-[-12px] before:left-8 before:border-8 before:border-transparent before:border-t-white';
            case 'dramatic':
                return 'bg-gradient-to-r from-purple-900/90 via-indigo-900/90 to-purple-900/90 py-4 px-6 text-center font-bold text-xl text-white tracking-wide';
            case 'caption':
            default:
                return 'mx-4 bg-black/70 backdrop-blur-sm rounded-xl p-4 text-white';
        }
    };

    if (isLoading) {
        return (
            <div className="relative w-full aspect-video bg-gradient-to-br from-primary-100 via-blue-50 to-indigo-100 rounded-2xl overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                        <div className="text-5xl mb-3 animate-bounce">🎨</div>
                        <p className="text-gray-600 font-medium">Generating scene...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="relative w-full aspect-video rounded-2xl overflow-hidden shadow-xl">
            {/* Scene Image with gradient fallback */}
            {imageUrl ? (
                <img
                    src={imageUrl}
                    alt="Story scene"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                        const parent = (e.target as HTMLImageElement).parentElement;
                        if (parent) {
                            (e.target as HTMLImageElement).style.display = 'none';
                            const div = document.createElement('div');
                            div.className = 'w-full h-full flex items-center justify-center bg-gradient-to-br from-primary-400 via-indigo-400 to-purple-500';
                            div.innerHTML = '<span style="font-size:5rem">📖</span>';
                            parent.insertBefore(div, parent.firstChild);
                        }
                    }}
                />
            ) : (
                <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-primary-400 via-indigo-400 to-purple-500">
                    <span className="text-7xl">📖</span>
                </div>
            )}

            {/* Text Overlay */}
            {textOverlay && textOverlay.text && (
                <div className={`absolute ${getPositionClass(textOverlay.position)}`}>
                    <div className={getStyleClass(textOverlay.style)}>
                        {textOverlay.text}
                    </div>
                </div>
            )}
        </div>
    );
};
