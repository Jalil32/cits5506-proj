// src/hooks/useVideos.ts
import { useState, useEffect } from "react";
import type { VideoData } from "../types";

export const useVideos = () => {
	const [videos, setVideos] = useState<VideoData[]>([]);
	const [selectedVideo, setSelectedVideo] = useState<VideoData | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	const fetchVideos = async () => {
		try {
			setLoading(true);
			// Use environment variable if available (for production), otherwise use localhost
			const apiUrl = "http://localhost:3000";
			const response = await fetch(`${apiUrl}/videos`);

			if (!response.ok) {
				throw new Error(`Error fetching videos: ${response.statusText}`);
			}

			const data = await response.json();

			// Convert string dates to Date objects
			const processedVideos = data.videos.map((video: any) => ({
				...video,
				lastModified: new Date(video.lastModified),
			}));

			// Sort videos by date (newest first)
			processedVideos.sort(
				(a: VideoData, b: VideoData) =>
					b.lastModified.getTime() - a.lastModified.getTime(),
			);

			setVideos(processedVideos);

			// If we have videos and none selected, select the first one
			if (processedVideos.length > 0 && !selectedVideo) {
				setSelectedVideo(processedVideos[0]);
			}

			setError(null);
		} catch (err) {
			console.error("Failed to fetch videos:", err);
			setError("Failed to load security footage. Please try again.");
		} finally {
			setLoading(false);
		}
	};

	useEffect(() => {
		fetchVideos();

		// Refresh the list every 5 minutes to get fresh pre-signed URLs
		const intervalId = setInterval(fetchVideos, 5 * 60 * 1000);

		return () => clearInterval(intervalId);
	}, []);

	const handleVideoError = () => {
		setError(
			"Error playing the video. The URL may have expired. Try refreshing the videos.",
		);
	};

	return {
		videos,
		selectedVideo,
		loading,
		error,
		fetchVideos,
		setSelectedVideo,
		handleVideoError,
	};
};
