// src/components/VideoSection.tsx
import type React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { Button } from "./ui/button";
import { RefreshCw } from "lucide-react";
import { VideoDisplay } from "./VideoDisplay";
import { VideoGallery } from "./VideoGallery";
import type { VideoData } from "../types";
import PrivacyMode from "./PrivacyMode";

interface VideoSectionProps {
	videos: VideoData[];
	selectedVideo: VideoData | null;
	loading: boolean;
	error: string | null;
	privacyMode: boolean;
	onRefresh: () => void;
	onSelectVideo: (video: VideoData) => void;
	onVideoError: () => void;
	onTogglePrivacy: () => void;
}

export const VideoSection: React.FC<VideoSectionProps> = ({
	videos,
	selectedVideo,
	loading,
	error,
	privacyMode,
	onRefresh,
	onSelectVideo,
	onVideoError,
	onTogglePrivacy,
}) => {
	return (
		<Card className="flex flex-1 bg-zinc-900 border-zinc-800 min-w-0">
			<PrivacyMode />
			<CardHeader className="flex-wrap">
				<CardTitle className="text-zinc-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 w-full">
					<span className="truncate">Home Security Monitoring</span>
					{error && (
						<span className="text-red-500 text-sm truncate">{error}</span>
					)}
					<Button
						variant="outline"
						size="sm"
						onClick={onRefresh}
						disabled={loading}
						className="text-zinc-100 border-zinc-700 hover:bg-zinc-800 shrink-0"
					>
						<RefreshCw
							className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`}
						/>
						{loading ? "Loading..." : "Refresh"}
					</Button>
				</CardTitle>
			</CardHeader>
			<CardContent className="space-y-4">
				<VideoDisplay
					selectedVideo={selectedVideo}
					privacyMode={privacyMode}
					onVideoError={onVideoError}
				/>

				{/* Privacy Mode Button */}
				<div className="flex justify-end">
					<Button
						variant={privacyMode ? "destructive" : "outline"}
						onClick={onTogglePrivacy}
						className="shrink-0"
					>
						Privacy Mode {privacyMode ? "ON" : "OFF"}
					</Button>
				</div>

				<VideoGallery
					videos={videos}
					loading={loading}
					onSelectVideo={onSelectVideo}
				/>
			</CardContent>
		</Card>
	);
};
