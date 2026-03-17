import React from 'react';
import { cn } from '../../utils/helpers';

interface ProgressBarProps {
  value: number;
  max: number;
  label?: string;
  showPercentage?: boolean;
  className?: string;
  color?: 'primary' | 'success' | 'warning' | 'danger';
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max,
  label,
  showPercentage = true,
  className,
  color = 'primary',
}) => {
  const percentage = Math.min((value / max) * 100, 100);

  const colors = {
    primary: 'bg-primary-600',
    success: 'bg-green-600',
    warning: 'bg-yellow-600',
    danger: 'bg-red-600',
  };

  return (
    <div className={cn('w-full', className)}>
      {(label || showPercentage) && (
        <div className="flex justify-between mb-1">
          {label && <span className="text-sm font-medium text-gray-700">{label}</span>}
          {showPercentage && (
            <span className="text-sm text-gray-600">{Math.round(percentage)}%</span>
          )}
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={cn('h-2.5 rounded-full transition-all duration-300', colors[color])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
