// src/components/VideoSection.tsx
import type React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { RefreshCw } from 'lucide-react';
import { VideoDisplay } from './VideoDisplay';
import { VideoGallery } from './VideoGallery';
import type { VideoData } from '../types';

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
            {error && (
                <span className="text-red-500 text-sm truncate">{error}</span>
            )}
            <CardContent className="space-y-4">
                <VideoDisplay
                    selectedVideo={selectedVideo}
                    privacyMode={privacyMode}
                    onVideoError={onVideoError}
                />

                {/* Privacy Mode Button */}
                <div className="flex justify-end">
                    <Button
                        variant={privacyMode ? 'destructive' : 'outline'}
                        onClick={onTogglePrivacy}
                        className="shrink-0"
                    >
                        Privacy Mode {privacyMode ? 'ON' : 'OFF'}
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
