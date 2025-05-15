import express, { type Request, type Response } from "express";
import iotService from "../services/iotService";

const router = express.Router();

// Initialize IoT service when server starts
iotService.connect();

// Interface for request with enabled property
interface SetPrivacyRequest extends Request {
	body: {
		enabled: boolean;
	};
}

// Route to get current privacy status
router.get("/status", (_: Request, res: Response) => {
	// Return the last known status or fetch it from the device
	const status = iotService.getLastStatus();
	res.json({
		success: true,
		status: status || {
			privacyModeEnabled: false,
			isConnected: iotService.isConnected(),
		},
	});
});

// Route to set privacy mode
router.post(
	"/set",
	async (req: SetPrivacyRequest, res: Response): Promise<void> => {
		try {
			const { enabled } = req.body;

			if (typeof enabled !== "boolean") {
				res.status(400).json({
					success: false,
					message: 'Missing or invalid "enabled" parameter',
				});
				return;
			}

			await iotService.setPrivacyMode(enabled);
			res.json({ success: true });
		} catch (err) {
			console.error("Error setting privacy mode:", err);
			const errorMessage =
				err instanceof Error ? err.message : "Failed to set privacy mode";
			res.status(500).json({
				success: false,
				message: errorMessage,
			});
		}
	},
);

export default router;
