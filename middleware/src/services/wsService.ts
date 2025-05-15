import WebSocket from "ws";
import type http from "node:http";
import iotService, { type PrivacyStatus } from "./iotService";

interface StatusMessage {
	type: string;
	data: PrivacyStatus;
}

function setupWebSocket(server: http.Server): WebSocket.Server {
	const wss = new WebSocket.Server({ server });

	wss.on("connection", (ws: WebSocket) => {
		console.log("WebSocket client connected");

		// Send initial status if available
		const initialStatus = iotService.getLastStatus();
		if (initialStatus) {
			const message: StatusMessage = {
				type: "privacy_status",
				data: initialStatus,
			};
			ws.send(JSON.stringify(message));
		}

		// Set up listener for status updates
		const removeListener = iotService.addStatusListener(
			(status: PrivacyStatus) => {
				if (ws.readyState === WebSocket.OPEN) {
					const message: StatusMessage = {
						type: "privacy_status",
						data: status,
					};
					ws.send(JSON.stringify(message));
				}
			},
		);

		// Clean up listener when connection closes
		ws.on("close", () => {
			console.log("WebSocket client disconnected");
			removeListener();
		});
	});

	return wss;
}

export default setupWebSocket;
