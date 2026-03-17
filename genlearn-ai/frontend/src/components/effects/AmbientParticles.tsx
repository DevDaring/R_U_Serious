import React, { useEffect, useMemo, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';
import type { ISourceOptions } from '@tsparticles/engine';

type AmbientTheme = 'snow' | 'rain' | 'sunny' | 'sparkle' | 'bubbles' | 'neural' | 'fireflies';

interface AmbientParticlesProps {
  theme: AmbientTheme;
  className?: string;
}

const themeConfigs: Record<AmbientTheme, ISourceOptions> = {
  snow: {
    fullScreen: false,
    particles: {
      number: { value: 40, density: { enable: true } },
      color: { value: '#cbd5e1' },
      shape: { type: 'circle' },
      opacity: { value: { min: 0.3, max: 0.7 } },
      size: { value: { min: 2, max: 6 } },
      move: {
        enable: true,
        speed: { min: 0.5, max: 1.5 },
        direction: 'bottom',
        straight: false,
        outModes: { default: 'out' },
      },
    },
    detectRetina: true,
  },
  rain: {
    fullScreen: false,
    particles: {
      number: { value: 60, density: { enable: true } },
      color: { value: '#93c5fd' },
      shape: { type: 'circle' },
      opacity: { value: { min: 0.2, max: 0.5 } },
      size: { value: { min: 1, max: 3 } },
      move: {
        enable: true,
        speed: { min: 3, max: 6 },
        direction: 'bottom',
        straight: true,
        outModes: { default: 'out' },
      },
    },
    detectRetina: true,
  },
  sunny: {
    fullScreen: false,
    particles: {
      number: { value: 20, density: { enable: true } },
      color: { value: ['#fbbf24', '#f59e0b', '#fcd34d'] },
      shape: { type: 'circle' },
      opacity: { value: { min: 0.1, max: 0.4 }, animation: { enable: true, speed: 0.5 } },
      size: { value: { min: 3, max: 12 }, animation: { enable: true, speed: 2 } },
      move: {
        enable: true,
        speed: { min: 0.2, max: 0.8 },
        direction: 'none',
        random: true,
        outModes: { default: 'bounce' },
      },
    },
    detectRetina: true,
  },
  sparkle: {
    fullScreen: false,
    particles: {
      number: { value: 30, density: { enable: true } },
      color: { value: ['#a78bfa', '#818cf8', '#c084fc', '#e879f9'] },
      shape: { type: 'star' },
      opacity: { value: { min: 0.2, max: 0.8 }, animation: { enable: true, speed: 1 } },
      size: { value: { min: 2, max: 5 }, animation: { enable: true, speed: 2 } },
      move: {
        enable: true,
        speed: { min: 0.3, max: 1 },
        direction: 'none',
        random: true,
        outModes: { default: 'bounce' },
      },
    },
    detectRetina: true,
  },
  bubbles: {
    fullScreen: false,
    particles: {
      number: { value: 25, density: { enable: true } },
      color: { value: ['#67e8f9', '#a5f3fc', '#22d3ee'] },
      shape: { type: 'circle' },
      opacity: { value: { min: 0.1, max: 0.4 } },
      size: { value: { min: 4, max: 15 }, animation: { enable: true, speed: 3 } },
      move: {
        enable: true,
        speed: { min: 0.3, max: 1 },
        direction: 'top',
        random: true,
        outModes: { default: 'out' },
      },
    },
    detectRetina: true,
  },
  neural: {
    fullScreen: false,
    particles: {
      number: { value: 35, density: { enable: true } },
      color: { value: '#818cf8' },
      shape: { type: 'circle' },
      opacity: { value: { min: 0.2, max: 0.5 } },
      size: { value: { min: 1, max: 4 } },
      links: {
        enable: true,
        color: '#818cf8',
        distance: 120,
        opacity: 0.15,
        width: 1,
      },
      move: {
        enable: true,
        speed: { min: 0.3, max: 0.8 },
        direction: 'none',
        outModes: { default: 'bounce' },
      },
    },
    detectRetina: true,
  },
  fireflies: {
    fullScreen: false,
    particles: {
      number: { value: 15, density: { enable: true } },
      color: { value: ['#fbbf24', '#34d399', '#60a5fa'] },
      shape: { type: 'circle' },
      opacity: { value: { min: 0, max: 0.8 }, animation: { enable: true, speed: 0.8 } },
      size: { value: { min: 2, max: 6 } },
      move: {
        enable: true,
        speed: { min: 0.2, max: 0.6 },
        direction: 'none',
        random: true,
        outModes: { default: 'bounce' },
      },
    },
    detectRetina: true,
  },
};

// Track initialization globally
let engineInitialized = false;
let initPromise: Promise<void> | null = null;

export const AmbientParticles: React.FC<AmbientParticlesProps> = ({ theme, className = '' }) => {
  const [ready, setReady] = useState(engineInitialized);

  useEffect(() => {
    if (engineInitialized) {
      setReady(true);
      return;
    }
    if (!initPromise) {
      initPromise = initParticlesEngine(async (engine) => {
        await loadSlim(engine);
      }).then(() => {
        engineInitialized = true;
      });
    }
    initPromise.then(() => setReady(true));
  }, []);

  const options = useMemo(() => themeConfigs[theme], [theme]);

  if (!ready) return null;

  return (
    <div className={`absolute inset-0 pointer-events-none overflow-hidden ${className}`}>
      <Particles
        id={`particles-${theme}`}
        options={options}
        className="absolute inset-0"
      />
    </div>
  );
};
