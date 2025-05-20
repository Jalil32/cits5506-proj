import { useState, useEffect } from "react";
import axios from "axios";
import { Switch } from "@headlessui/react";

// Define interfaces for the component
interface PrivacyStatus {
	privacyModeEnabled: boolean;
	deviceId?: string;
	lastStateChange?: string;
	isRecording?: boolean;
}

interface WebSocketMessage {
	type: string;
	data: PrivacyStatus;
}

const PrivacyMode: React.FC = () => {
	const [privacyEnabled, setPrivacyEnabled] = useState<boolean>(false);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);
	const [socket, setSocket] = useState<WebSocket | null>(null); // Initialize WebSocket connection

	useEffect(() => {
		const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
		const ws = new WebSocket(`${wsProtocol}//${window.location.host}`);

		ws.onopen = () => {
			console.log("WebSocket connected");
		};

		ws.onmessage = (event) => {
			try {
				const message = JSON.parse(event.data) as WebSocketMessage;
				if (message.type === "privacy_status") {
					setPrivacyEnabled(message.data.privacyModeEnabled);
					setLoading(false);
				}
			} catch (err) {
				console.error("Error parsing WebSocket message:", err);
			}
		};

		ws.onerror = (error) => {
			console.error("WebSocket error:", error);
			setError("Connection error");
		};

		setSocket(ws);

		// Fetch initial status
		fetchStatus();

		// Clean up on unmount
		return () => {
			if (ws) {
				ws.close();
			}
		};
	}, []);

	// Fetch current privacy status
	const fetchStatus = async (): Promise<void> => {
		try {
			setLoading(true);
			const response = await axios.get<{
				success: boolean;
				status: PrivacyStatus;
			}>("http://localhost:3000/status");

			if (response.data.success) {
				setPrivacyEnabled(response.data.status.privacyModeEnabled);
			} else {
				setError("Failed to get status");
			}
		} catch (err) {
			console.error("Error fetching privacy status:", err);
			setError("Failed to load status");
		} finally {
			setLoading(false);
		}
	};

	// Toggle privacy mode
	const handleToggle = async (): Promise<void> => {
		try {
			// Set loading state
			setLoading(true);
			// We toggle based on the current state, not based on a passed parameter
			const newState = !privacyEnabled;
			
			const response = await axios.post<{
				success: boolean;
				status?: PrivacyStatus;
			}>(
				"http://localhost:3000/set",
				{ enabled: newState },
			);

			if (response.data.success) {
				// Only update the state when we receive confirmation from the server
				if (response.data.status) {
					// If the server returns the updated status, use that
					setPrivacyEnabled(response.data.status.privacyModeEnabled);
				} else {
					// Otherwise use the state we sent
					setPrivacyEnabled(newState);
				}
			} else {
				setError("Failed to set privacy mode");
				// No need to revert the state as we haven't changed it yet
			}
		} catch (err) {
			console.error("Error setting privacy mode:", err);
			setError("Failed to set privacy mode");
			// No need to revert as we haven't changed it yet
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className=" rounded-lg ml-4">
			<h2 className="text-2xl font-semibold  mb-4">
				Privacy Mode
			</h2>

			{error && (
				<div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4 rounded">
					<div className="flex items-center justify-between">
						<p className="text-red-700">{error}</p>
						<button
							onClick={() => {
								setError(null);
								fetchStatus();
							}}
							className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
						>
							Retry
						</button>
					</div>
				</div>
			)}

			<div className="flex items-center justify-between py-4 border-b border-gray-200">
				<div className="flex flex-col">
					<span
						className={`text-lg font-medium ${privacyEnabled ? "text-blue-600" : ""}`}
					>
						{privacyEnabled ? "Privacy Mode ON" : "Privacy Mode OFF"}
					</span>
					<span className="text-sm  mt-1">
						{privacyEnabled
							? "Motion detection and recording are paused"
							: "Motion detection and recording are active"}
					</span>
				</div>

				<div className="flex items-center">
					{loading && (
						<div className="mr-3">
							<div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
						</div>
					)}

					<Switch
						checked={privacyEnabled}
						onChange={handleToggle}
						disabled={loading}
						className={`${
							privacyEnabled ? "bg-blue-600" : "bg-gray-300"
						} relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
							loading ? "opacity-50 cursor-not-allowed" : ""
						}`}
					>
						<span
							className={`${
								privacyEnabled ? "translate-x-6" : "translate-x-1"
							} inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
						/>
					</Switch>
				</div>
			</div>

			<div className="mt-4 p-4 bg-gray-50 rounded-md">
				<h3 className="text-md font-medium text-gray-700 mb-2">
					About Privacy Mode
				</h3>
				<p className="text-gray-600 text-sm">
					{privacyEnabled ? (
						<>
							Privacy mode is currently{" "}
							<span className="font-semibold text-blue-600">active</span>. Your
							camera will not detect motion or record videos until you disable
							privacy mode.
						</>
					) : (
						<>
							Privacy mode is currently{" "}
							<span className="font-semibold text-gray-600">inactive</span>.
							Your camera is monitoring for motion and will record videos when
							motion is detected.
						</>
					)}
				</p>
			</div>
		</div>
	);
};

export default PrivacyMode;
