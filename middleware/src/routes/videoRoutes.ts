import {
	GetObjectCommand,
	ListObjectsV2Command,
	S3Client,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import express, { type Request, type Response } from "express";
import dotenv from "dotenv";
import path from "node:path";
dotenv.config();
const videoRoutes = express.Router();
// Configure the S3 client
const s3Client = new S3Client({
	region: process.env.AWS_REGION || "",
	credentials: {
		accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
		secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
	},
});
// Define the bucket name
const BUCKET_NAME = process.env.S3_BUCKET_NAME || "my_bucket_name";

videoRoutes.get("/videos", async (_: Request, res: Response): Promise<void> => {
	try {
		const params = {
			Bucket: BUCKET_NAME,
			Prefix: "clips/",
			MaxKeys: 1000,
		};
		// List all objects in the bucket
		const listCommand = new ListObjectsV2Command(params);
		const data = await s3Client.send(listCommand);
		// If no contents found
		if (!data.Contents || data.Contents.length === 0) {
			res.status(200).json({ videos: [] });
			return;
		}
		// Filter for video files (assuming common video extensions)
		const videoExtensions = [".mp4", ".avi", ".mov", ".mkv", ".webm"];
		const videoFiles = data.Contents.filter((item) =>
			videoExtensions.some((ext) => item.Key?.toLowerCase().endsWith(ext)),
		);
		// Generate signed URLs for each video file (valid for 1 hour)
		const videos = await Promise.all(
			videoFiles.map(async (file) => {
				const getObjectParams = {
					Bucket: BUCKET_NAME,
					Key: file.Key,
				};
				const command = new GetObjectCommand(getObjectParams);
				const signedUrl = await getSignedUrl(s3Client, command, {
					expiresIn: 3600,
				});

				// Extract filename from the full path
				const filename = file.Key?.split("/").pop() || file.Key;

				// Generate thumbnail URL
				// Extract the date part from the filename (assuming format like 20250520_024522.mp4)
				let thumbnailUrl = "";
				const dateMatch = filename!.match(/(\d{8}_\d{6})/);
				if (dateMatch) {
					const dateStr = dateMatch[1];
					// Create a signed URL for the thumbnail
					const thumbnailKey = `frames/${dateStr}/frame_0.jpg`;
					const thumbnailCommand = new GetObjectCommand({
						Bucket: BUCKET_NAME,
						Key: thumbnailKey,
					});
					try {
						thumbnailUrl = await getSignedUrl(s3Client, thumbnailCommand, {
							expiresIn: 3600,
						});
					} catch (err) {
						console.warn(`Thumbnail not found for ${filename}:`, err);
					}
				}

				return {
					key: file.Key,
					filename,
					size: file.Size,
					lastModified: file.LastModified,
					url: signedUrl,
					thumbnailUrl, // Add the thumbnail URL to the response
				};
			}),
		);
		// Sort videos by last modified date (newest first)
		videos.sort((a, b) => {
			const dateA = a.lastModified ? new Date(a.lastModified).getTime() : 0;
			const dateB = b.lastModified ? new Date(b.lastModified).getTime() : 0;
			return dateB - dateA;
		});
		res.status(200).json({ videos });
	} catch (error) {
		console.error("Error fetching videos from S3:", error);
		res.status(500).json({
			error: "Failed to fetch videos",
			message: (error as Error).message,
		});
	}
});

// Handle thumbnail requests for a specific date and frame
videoRoutes.get(
	"/thumbnails/frames/:dateStr/frame_:frameNum.jpg",
	async (req: Request, res: Response): Promise<void> => {
		try {
			const { dateStr, frameNum } = req.params;

			// Validate the date string format (YYYYMMDD_HHMMSS)
			if (!dateStr.match(/^\d{8}_\d{6}$/)) {
				res.status(400).json({ error: "Invalid date format" });
				return;
			}

			// Construct the S3 key
			const objectKey = `frames/${dateStr}/frame_${frameNum}.jpg`;

			const getObjectParams = {
				Bucket: BUCKET_NAME,
				Key: objectKey,
			};

			// Generate signed URL for the thumbnail
			const command = new GetObjectCommand(getObjectParams);
			const signedUrl = await getSignedUrl(s3Client, command, {
				expiresIn: 3600,
			});

			// Add cache control headers (optional)
			res.set("Cache-Control", "public, max-age=86400"); // Cache for 24 hours

			// Redirect to the signed URL
			res.redirect(signedUrl);
		} catch (error) {
			console.error("Error fetching thumbnail from S3:", error);

			// Send a default thumbnail or error response
			res.status(404).json({
				error: "Thumbnail not found",
				message: (error as Error).message,
			});
		}
	},
);

export default videoRoutes;
