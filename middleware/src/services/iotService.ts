import { device as IoTDevice } from "aws-iot-device-sdk";
import * as path from "node:path";
import { EventEmitter } from "events";

// Define your certificate paths - adjust as needed
const CERT_PATH = path.join(__dirname, "../../certs");
const CERT_FILE = path.join(CERT_PATH, "root.pem");
const KEY_FILE = path.join(
	CERT_PATH,
	"1861f71c931055d2efb5687c16278b1e4bdda96a39a7aaa1f3636b3fe592f2ee-private.pem.key",
);
const CA_FILE = path.join(CERT_PATH, "AmazonRootCA1.pem");

// AWS IoT Configuration
const IOT_ENDPOINT = "a3e9lka9w5gk8f-ats.iot.ap-southeast-2.amazonaws.com";
const CLIENT_ID = "web_app_client";

// Topics
const PRIVACY_COMMAND_TOPIC = "home/cameras/privacy/command";
const PRIVACY_STATUS_TOPIC = "home/cameras/privacy/status";
const NOTIFICATION_TOPIC = "home/cameras/notification";

// Interfaces
export interface PrivacyStatus {
	privacyModeEnabled: boolean;
	deviceId: string;
	lastStateChange: string;
	isRecording: boolean;
}

export interface Notification {
	message: string;
	type: "info" | "success" | "warning" | "error";
	timestamp: string;
	deviceId?: string;
	metadata?: Record<string, any>;
}

type StatusListener = (status: PrivacyStatus) => void;
type NotificationListener = (notification: Notification) => void;

class IoTService extends EventEmitter {
	private device: InstanceType<typeof IoTDevice> | null = null;
	private connected: boolean = false;
	private statusListeners: StatusListener[] = [];
	private notificationListeners: NotificationListener[] = [];
	private lastStatus: PrivacyStatus | null = null;

	public connect(): void {
		try {
			// Create the MQTT device object
			this.device = new IoTDevice({
				keyPath: KEY_FILE,
				certPath: CERT_FILE,
				caPath: CA_FILE,
				clientId: CLIENT_ID,
				host: IOT_ENDPOINT,
				keepalive: 10,
			});

			// Set up event handlers
			this.device.on("connect", () => {
				console.log("Connected to AWS IoT Core");
				this.connected = true;

				// Subscribe to topics to get updates
				if (this.device) {
					this.device.subscribe(PRIVACY_STATUS_TOPIC);
					this.device.subscribe(NOTIFICATION_TOPIC);
				}
			});

			this.device.on("message", (topic: string, payload: Buffer) => {
				if (topic === PRIVACY_STATUS_TOPIC) {
					try {
						const status = JSON.parse(payload.toString()) as PrivacyStatus;
						console.log("Received status update:", status);

						// Store the last status
						this.lastStatus = status;

						// Notify all listeners
						this.statusListeners.forEach((listener) => {
							listener(status);
						});

						// Emit event for WebSocket relay
						this.emit("privacyStatusUpdate", status);
					} catch (err) {
						console.error("Error parsing status message:", err);
					}
				} else if (topic === NOTIFICATION_TOPIC) {
					try {
						const notification = JSON.parse(payload.toString()) as Notification;
						console.log("Received notification:", notification);

						// Notify all notification listeners
						this.notificationListeners.forEach((listener) => {
							listener(notification);
						});

						// Emit event for WebSocket relay
						this.emit("notification", notification);
					} catch (err) {
						console.error("Error parsing notification:", err);
					}
				}
			});

			this.device.on("error", (error: string | Error) => {
				console.error("IoT error:", error);
				this.connected = false;
			});

			this.device.on("offline", () => {
				console.log("IoT device went offline");
				this.connected = false;
			});

			this.device.on("reconnect", () => {
				console.log("IoT device reconnecting...");
			});
		} catch (error) {
			console.error("Error connecting to AWS IoT:", error);
			this.connected = false;
		}
	}

	// Set privacy mode
	public setPrivacyMode(enabled: boolean): Promise<void> {
		if (!this.connected || !this.device) {
			throw new Error("Not connected to AWS IoT");
		}

		const message = JSON.stringify({
			privacyModeEnabled: enabled,
		});

		return new Promise<void>((resolve, reject) => {
			if (this.device) {
				this.device.publish(
					PRIVACY_COMMAND_TOPIC,
					message,
					{ qos: 1 },
					(err?: Error) => {
						if (err) {
							console.error("Error publishing privacy command:", err);
							reject(err);
						} else {
							console.log(`Privacy mode ${enabled ? "enabled" : "disabled"}`);
							resolve();
						}
					},
				);
			} else {
				reject(new Error("Device not initialized"));
			}
		});
	}

	// Add a listener for status updates
	public addStatusListener(listener: StatusListener): () => void {
		this.statusListeners.push(listener);
		return () => {
			this.statusListeners = this.statusListeners.filter((l) => l !== listener);
		};
	}

	// Add a listener for notification updates
	public addNotificationListener(listener: NotificationListener): () => void {
		this.notificationListeners.push(listener);
		return () => {
			this.notificationListeners = this.notificationListeners.filter(
				(l) => l !== listener,
			);
		};
	}

	// Get the last known status
	public getLastStatus(): PrivacyStatus | null {
		return this.lastStatus;
	}

	// Check if connected to IoT Core
	public isConnected(): boolean {
		return this.connected;
	}
}

// Create and export a singleton instance
const iotService = new IoTService();
export default iotService;
