import type React from 'react';
import { VideoDisplay } from './VideoDisplay';
import { VideoGallery } from './VideoGallery';
import type { VideoData } from '../types';
import { Button } from './ui/button';
import { Download, Clock, FileText, HardDrive } from 'lucide-react';
import { formatDetailedDate, formatFileSize } from '../utils/formatters';

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
    onSelectVideo,
    onVideoError,
}) => {
    return (
        <div className="flex flex-1 gap-4">
            <div className="flex-1 flex flex-col">
                {error && (
                    <div className="bg-red-900/20 border border-red-900 text-red-400 px-4 py-2 rounded-md mb-4">
                        {error}
                    </div>
                )}
                
                <VideoDisplay
                    selectedVideo={selectedVideo}
                    privacyMode={privacyMode}
                    onVideoError={onVideoError}
                />
                
                {selectedVideo && !privacyMode && (
                    <div className="mt-4  rounded-lg p-4">
                        {/* Title and download button */}
                        <div className="flex justify-between items-start mb-3">
                            <h1 className="text-lg font-semibold ">
                                {selectedVideo.filename || `Recording ${selectedVideo.key}`}
                            </h1>
                            <Button 
                                variant="outline" 
                                className="border-zinc-700  "
                            >
                                <Download className="h-4 w-4 mr-2" />
                                <a 
                                    href={selectedVideo.url}
                                    download={selectedVideo.filename || `recording-${selectedVideo.key}.mp4`}
                                    className="no-underline  "
                                >
                                    Download
                                </a>
                            </Button>
                        </div>
                        
                        {/* Video metadata */}
                        <div className="flex flex-wrap gap-4 border-t border-b  py-3">
                            <div className="flex items-center ">
                                <Clock className="h-4 w-4 mr-2" />
                                <span className="text-sm">
                                    {formatDetailedDate(selectedVideo.lastModified)}
                                </span>
                            </div>
                            
                            <div className="flex items-center">
                                <FileText className="h-4 w-4 mr-2" />
                                <span className="text-sm">
                                    {selectedVideo.filename || `recording-${selectedVideo.key}.mp4`}
                                </span>
                            </div>
                            
                            {selectedVideo.size && (
                                <div className="flex items-center ">
                                    <HardDrive className="h-4 w-4 mr-2" />
                                    <span className="text-sm">
                                        {formatFileSize(selectedVideo.size)}
                                    </span>
                                </div>
                            )}
                        </div>
                        
                        <div className="mt-3 text-sm">
                            <p>Security camera recording from {formatDetailedDate(selectedVideo.lastModified)}</p>
                        </div>
                    </div>
                )}
            </div>
            
            <VideoGallery
                selectedVideo={selectedVideo}
                videos={videos}
                loading={loading}
                onSelectVideo={onSelectVideo}
            />
        </div>
    );
};

// Helper function if formatFileSize doesn't exist in your utils
// You can move this to your formatters.ts file
