# R U Serious? Frontend

A modern, responsive frontend for the R U Serious? adaptive learning system built with React, TypeScript, Vite, and Tailwind CSS.

## Features

- **Modern Tech Stack**: React 18, TypeScript, Vite, Tailwind CSS
- **State Management**: Zustand for efficient state management
- **Routing**: React Router v6 for navigation
- **API Integration**: Axios with interceptors for authentication
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Type Safety**: Full TypeScript coverage
- **Component Library**: Reusable UI components
- **Voice Support**: Text-to-speech and speech-to-text capabilities
- **Real-time Chat**: AI assistant integration
- **Gamification**: Tournaments, teams, and leaderboards

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update the `.env` file with your API URL:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Development

Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Common components (Button, Modal, etc.)
│   ├── layout/         # Layout components (Navbar, Menu, etc.)
│   ├── auth/           # Authentication components
│   ├── learning/       # Learning session components
│   ├── avatar/         # Avatar creation components
│   ├── characters/     # Character management
│   ├── gamification/   # Tournaments, teams, leaderboard
│   ├── voice/          # Voice input/output components
│   ├── chat/           # Chat interface
│   └── admin/          # Admin panel components
├── pages/              # Page components
├── hooks/              # Custom React hooks
├── store/              # Zustand stores
├── services/           # API services
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── App.tsx             # Main app component
├── main.tsx            # App entry point
└── index.css           # Global styles
```

## Key Features

### Authentication
- JWT-based authentication
- Protected routes
- Auto token refresh
- Role-based access (admin/user)

### Learning Sessions
- Course configuration
- Image carousel with narratives
- MCQ quizzes
- Descriptive questions
- Video generation
- Progress tracking

### Gamification
- XP and leveling system
- Tournaments
- Team collaboration
- Global leaderboards
- Streak tracking

### Voice Features
- Text-to-speech narration
- Speech-to-text input
- Full vocal mode for accessibility
- Multi-language support

### Customization
- Avatar creation (draw/upload/gallery)
- Character management
- Theme customization
- Language preferences

## Default Credentials

For development/testing:
- **Admin**: username: `admin`, password: `password123`
- **User**: username: `john_doe`, password: `password123`

## Technologies Used

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **React Router**: Client-side routing
- **Axios**: HTTP client with interceptors
- **Fabric.js**: Canvas drawing capabilities

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the R U Serious? prototype system.
