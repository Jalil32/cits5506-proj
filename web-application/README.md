# IoT Security System Web Application

A modern React-based web application for monitoring and managing an IoT security camera system. Built with TypeScript, Vite, and Tailwind CSS.

## Features

- **Live Camera Streaming**: Real-time video feed from connected IoT cameras
- **Video Gallery**: Browse and view recorded video footage with thumbnail previews
- **Privacy Mode**: Toggle privacy settings for camera streams
- **Dark/Light Theme**: Responsive theme switching with system preference support
- **Real-time Notifications**: Live notification system for security events
- **Responsive Design**: Mobile-friendly interface with collapsible sidebar navigation

## Technology Stack

- **Frontend Framework**: React 19 with TypeScript
- **Build Tool**: Vite 6
- **Styling**: Tailwind CSS 4 with Radix UI components
- **Routing**: React Router DOM
- **Real-time Communication**: Socket.io Client
- **HTTP Client**: Axios
- **UI Components**: Custom components built on Radix UI primitives

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager

## Installation

1. Clone the repository and navigate to the web-application directory:
```bash
cd web-application
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components (buttons, cards, etc.)
│   ├── CameraStreamView.tsx
│   ├── VideoGallery.tsx
│   ├── NotificationPanel.tsx
│   └── ...
├── pages/              # Main application pages
│   ├── home.tsx        # Video gallery and management
│   └── LiveStream.tsx  # Live camera streaming
├── hooks/              # Custom React hooks
├── utils/              # Utility functions and contexts
├── types/              # TypeScript type definitions
└── lib/                # Library configurations
```

## Key Components

- **Home Page**: Main dashboard for viewing recorded videos and managing the system
- **Live Stream Page**: Real-time camera feed with privacy controls
- **Video Gallery**: Grid-based video browser with thumbnail support
- **Notification System**: Real-time alerts and system notifications
- **Theme Provider**: Dark/light mode support with persistence

## Configuration

The application uses Vite for build configuration and supports:
- Path aliases (`@/` maps to `src/`)
- TypeScript compilation
- Tailwind CSS processing
- React Fast Refresh

## Browser Support

Modern browsers with ES2015+ support including:
- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+
