import type React from 'react';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Maximize2, Video } from 'lucide-react';
import type { VideoData } from '../types';
import { formatDetailedDate } from '../utils/formatters';

interface VideoDisplayProps {
    selectedVideo: VideoData | null;
    privacyMode: boolean;
    onVideoError: () => void;
}

export const VideoDisplay: React.FC<VideoDisplayProps> = ({
    selectedVideo,
    privacyMode,
    onVideoError,
}) => {
    return (
        <div className="relative bg-zinc-800 rounded-lg overflow-hidden w-full h-[600px]">
            {selectedVideo && !privacyMode ? (
                <video
                    src={selectedVideo.url}
                    controls
                    className="w-full h-full object-contain"
                    onError={onVideoError}
                />
            ) : (
                <div className="w-full h-full flex items-center justify-center">
                    {privacyMode ? (
                        <div className="text-center">
                            <Video className="h-12 text-zinc-600 mx-auto mb-2" />
                            <p className="text-zinc-400">
                                Privacy Mode Enabled
                            </p>
                        </div>
                    ) : (
                        <div className="text-center">
                            <Video className="h-12 text-zinc-600 mx-auto mb-2" />
                            <p className="text-zinc-400">
                                Select a video to play
                            </p>
                        </div>
                    )}
                </div>
            )}
            {selectedVideo && !privacyMode && (
                <Badge
                    variant="secondary"
                    className="absolute top-2 left-2 bg-zinc-700"
                >
                    {formatDetailedDate(selectedVideo.lastModified)}
                </Badge>
            )}
        </div>
    );
};
