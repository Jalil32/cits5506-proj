import express from "express";
import http from "node:http";
import { Server } from "socket.io";
import privacyRouter from "./routes/privacyRoutes";
import videoRoutes from "./routes/videoRoutes";
import cors from "cors";
import iotService, { type Notification } from "./services/iotService";

// 1) Initialize express app
const app = express();
const port = process.env.PORT || 3000;

// Create HTTP server instance from Express app
const server = http.createServer(app);

// Initialize Socket.IO with CORS configuration
const io = new Server(server, {
	cors: {
		// Use the same CORS configuration as your Express app
		origin:
			process.env.NODE_ENV === "production"
				? process.env.FRONTEND_URL
				: "http://localhost:5173",
		methods: ["GET", "POST"],
		credentials: true,
	},
});

// 2) Setup CORS for Express routes
app.use(
	cors({
		// During development, allow requests from React's dev server
		origin:
			process.env.NODE_ENV === "production"
				? process.env.FRONTEND_URL
				: "http://localhost:5173",
		methods: ["GET", "POST"],
		credentials: true,
	}),
);

// 2) Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(videoRoutes);
app.use(privacyRouter);

// Connect IoT service
iotService.connect();

// Listen for IoT notification events and relay them to connected clients
iotService.on("notification", (notification: Notification) => {
	io.emit("camera-notification", notification);
});

// Listen for IoT privacy status updates and relay them to connected clients
iotService.on("privacyStatusUpdate", (status) => {
	io.emit("privacy-status", status);
});

// Socket.IO connection handler
io.on("connection", (socket) => {
	console.log("Client connected:", socket.id);

	// Send the current privacy status when a client connects
	const currentStatus = iotService.getLastStatus();
	if (currentStatus) {
		socket.emit("privacy-status", currentStatus);
	}

	// Handle client disconnect
	socket.on("disconnect", () => {
		console.log("Client disconnected:", socket.id);
	});
});

// 3) Start the server - use the HTTP server instead of Express app
server.listen(port, () => {
	console.log(`Server running at http://localhost:${port}`);
	console.log(`WebSocket server listening for connections`);
});

export default server;
