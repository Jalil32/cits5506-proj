# Middleware

A Node.js Express server that acts as middleware between IoT camera devices, AWS services, and a web application frontend. This middleware handles video streaming, privacy controls, real-time notifications, and AWS S3 integration for video storage and retrieval.

## Features

- **Video Management**: List and serve videos from AWS S3 with signed URLs
- **Thumbnail Support**: Generate and serve video thumbnails 
- **Privacy Controls**: Toggle camera privacy mode via IoT commands
- **Real-time Communication**: WebSocket and Socket.IO for live updates
- **AWS IoT Integration**: MQTT communication with edge devices
- **Notification System**: Real-time camera notifications

## Tech Stack

- **Runtime**: Node.js with TypeScript
- **Framework**: Express.js
- **Real-time**: Socket.IO & WebSocket
- **Cloud**: AWS S3, AWS IoT Core
- **Code Quality**: Biome for linting and formatting

## Prerequisites

- Node.js (v18 or higher)
- AWS account with S3 and IoT Core configured
- AWS IoT certificates for device authentication

## Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS credentials and configuration
```

Required environment variables:
- `AWS_REGION`
- `AWS_ACCESS_KEY_ID` 
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET_NAME`
- `PORT` (optional, defaults to 3000)
- `NODE_ENV`
- `FRONTEND_URL` (for production CORS)

3. Place AWS IoT certificates in the `certs/` directory:
   - `root.pem`
   - `[device-private-key].pem.key`
   - `AmazonRootCA1.pem`

## Usage

### Development
```bash
npm run dev
```

### Production
```bash
npm run build
npm start
```

The server will start on `http://localhost:3000` (or your specified PORT).

## API Endpoints

### Video Routes
- `GET /videos` - List all videos from S3 with signed URLs and thumbnails
- `GET /thumbnails/frames/:dateStr/frame_:frameNum.jpg` - Serve specific video thumbnail

### Privacy Routes  
- `GET /status` - Get current camera privacy status
- `POST /set` - Set privacy mode (`{"enabled": true/false}`)

## WebSocket Events

The server emits the following Socket.IO events:
- `camera-notification` - Camera notifications from IoT devices
- `privacy-status` - Privacy mode status updates

## AWS IoT Topics

- `home/cameras/privacy/command` - Send privacy commands to devices
- `home/cameras/privacy/status` - Receive privacy status updates
- `home/cameras/notification` - Receive camera notifications

## Project Structure

```
src/
├── routes/
│   ├── videoRoutes.ts    # S3 video and thumbnail endpoints
│   └── privacyRoutes.ts  # Privacy control endpoints
├── services/
│   ├── iotService.ts     # AWS IoT Core communication
│   └── wsService.ts      # WebSocket service setup
├── types/
│   └── aws-iot-sdk.d.ts  # TypeScript definitions
└── server.ts             # Main server setup
```

## Development

- **Linting**: Uses Biome for code quality
- **TypeScript**: Full TypeScript support with strict typing
- **Hot Reload**: ts-node for development with automatic reloading

## License

ISC
