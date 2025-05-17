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
        <div className="relative bg-zinc-800 h-64 md:h-80 rounded-lg overflow-hidden">
            {selectedVideo && !privacyMode ? (
                <video
                    src={selectedVideo.url}
                    controls
                    className=" h-full object-contain"
                    onError={onVideoError}
                />
            ) : (
                <div className="h-full flex items-center justify-center">
                    {privacyMode ? (
                        <div className="text-center">
                            <Video className="h-12  text-zinc-600 mx-auto mb-2" />
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

            <Button
                variant="ghost"
                size="icon"
                className="absolute top-2 right-2 text-zinc-100 hover:bg-zinc-700"
                onClick={() => {
                    if (selectedVideo && !privacyMode) {
                        window.open(selectedVideo.url, '_blank');
                    }
                }}
                disabled={!selectedVideo || privacyMode}
            >
                <Maximize2 className="h-4 w-4" />
            </Button>
        </div>
    );
};
