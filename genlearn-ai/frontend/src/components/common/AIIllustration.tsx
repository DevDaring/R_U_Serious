import React from 'react';

interface IllustrationElement {
  label: string;
  detail: string;
  icon: string;
}

export interface IllustrationData {
  title: string;
  description: string;
  visual_type: string;
  emoji_icon: string;
  elements: IllustrationElement[];
  key_insight: string;
  gradient?: [string, string];
  turn_number?: number;
}

interface AIIllustrationProps {
  data: IllustrationData;
  compact?: boolean;
}

const typeLabels: Record<string, { label: string; icon: string }> = {
  diagram: { label: 'Diagram', icon: '📊' },
  concept_map: { label: 'Concept Map', icon: '🗺️' },
  comparison: { label: 'Comparison', icon: '⚖️' },
  process: { label: 'Process Flow', icon: '🔄' },
  analogy: { label: 'Analogy', icon: '🔗' },
  formula: { label: 'Formula', icon: '📐' },
  example: { label: 'Example', icon: '💡' },
  timeline: { label: 'Timeline', icon: '📅' },
};

export const AIIllustration: React.FC<AIIllustrationProps> = ({ data, compact = false }) => {
  const gradient = data.gradient || ['#667eea', '#764ba2'];
  const typeInfo = typeLabels[data.visual_type] || { label: data.visual_type, icon: '📌' };

  if (compact) {
    return (
      <div
        className="rounded-lg p-3 text-white relative overflow-hidden"
        style={{
          background: `linear-gradient(135deg, ${gradient[0]}, ${gradient[1]})`,
        }}
      >
        <div className="absolute inset-0 opacity-10">
          <div className="absolute -top-4 -right-4 text-8xl">{data.emoji_icon}</div>
        </div>
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg">{data.emoji_icon}</span>
            <span className="font-bold text-sm">{data.title}</span>
          </div>
          <p className="text-xs opacity-90">{data.key_insight}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl overflow-hidden shadow-lg border border-gray-100 my-3">
      {/* Header with gradient */}
      <div
        className="p-4 text-white relative overflow-hidden"
        style={{
          background: `linear-gradient(135deg, ${gradient[0]}, ${gradient[1]})`,
        }}
      >
        <div className="absolute inset-0 opacity-10">
          <div className="absolute -top-6 -right-6 text-[120px] leading-none">{data.emoji_icon}</div>
        </div>
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-1">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{data.emoji_icon}</span>
              <h3 className="font-bold text-lg">{data.title}</h3>
            </div>
            <span className="text-xs px-2 py-1 bg-white/20 rounded-full backdrop-blur-sm">
              {typeInfo.icon} {typeInfo.label}
            </span>
          </div>
          <p className="text-sm opacity-90">{data.description}</p>
        </div>
      </div>

      {/* Visual Elements */}
      <div className="p-4 bg-white space-y-2">
        {data.elements.map((el, idx) => (
          <div
            key={idx}
            className="flex items-start gap-3 p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
          >
            <span className="text-2xl flex-shrink-0 mt-0.5">{el.icon}</span>
            <div>
              <h4 className="font-semibold text-gray-800 text-sm">{el.label}</h4>
              <p className="text-xs text-gray-600">{el.detail}</p>
            </div>
            {data.visual_type === 'process' && idx < data.elements.length - 1 && (
              <span className="text-gray-300 ml-auto text-lg">→</span>
            )}
          </div>
        ))}
      </div>

      {/* Key Insight Footer */}
      <div
        className="px-4 py-3 border-t"
        style={{
          background: `linear-gradient(135deg, ${gradient[0]}10, ${gradient[1]}10)`,
        }}
      >
        <div className="flex items-center gap-2">
          <span className="text-sm">💡</span>
          <p className="text-sm font-medium text-gray-700">{data.key_insight}</p>
        </div>
      </div>
    </div>
  );
};
