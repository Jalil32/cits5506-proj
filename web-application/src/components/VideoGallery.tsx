// src/components/VideoGallery.tsx
import type React from "react";
import { ScrollArea } from "./ui/scroll-area";
import { VideoPlayer } from "./VideoPlayer";
import type { VideoData } from "../types";

interface VideoGalleryProps {
	videos: VideoData[];
	loading: boolean;
	onSelectVideo: (video: VideoData) => void;
}

export const VideoGallery: React.FC<VideoGalleryProps> = ({
	videos,
	loading,
	onSelectVideo,
}) => {
	return (
		<div className="flex-1 w-full flex flex-col">
			<h3 className="font-semibold mb-4 text-zinc-100">
				Security Camera Recordings
			</h3>
			<ScrollArea className="w-full ">
				<div className="flex gap-4 py-2 px-1 w-max">
					{loading && videos.length === 0 ? (
						<div className="flex items-center justify-center h-24 w-full">
							<p className="text-zinc-400">Loading videos...</p>
						</div>
					) : videos.length === 0 ? (
						<div className="flex items-center justify-center h-24 w-full">
							<p className="text-zinc-400">No security footage available</p>
						</div>
					) : (
						videos.map((video) => (
							<div key={video.key} className="shrink-0">
								<VideoPlayer
									video={video}
									onClick={() => onSelectVideo(video)}
								/>
							</div>
						))
					)}
				</div>
			</ScrollArea>
		</div>
	);
};
