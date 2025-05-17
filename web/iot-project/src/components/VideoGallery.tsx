import type React from 'react';
import { VideoPlayer } from './VideoPlayer';
import type { VideoData } from '../types';
import { ScrollArea } from './ui/scroll-area';
import { Video } from 'lucide-react';
import { formatDetailedDate } from '../utils/formatters';

interface VideoGalleryProps {
    videos: VideoData[];
    loading: boolean;
    onSelectVideo: (video: VideoData) => void;
    selectedVideo: VideoData | null;
}

export const VideoGallery: React.FC<VideoGalleryProps> = ({
    videos,
    loading,
    onSelectVideo,
    selectedVideo,
}) => {
    return (
        <div className="pl-4 lg:w-80 shrink-0">
            <div>
                <ScrollArea className=" h-[70vh]  md:h-[70vh] lg:h-[calc(100vh-9rem)]">

                    {loading && videos.length === 0 ? (
                        <div className="flex items-center justify-center h-24">
                            <p className="">Loading videos...</p>
                        </div>
                    ) : videos.length === 0 ? (
                        <div className="flex items-center justify-center h-24">
                            <p className="">No security footage available</p>
                        </div>
                    ) : (
                        <div className="flex flex-col gap-3 ">
                            {videos.map((video) => (
                                <div 
                                    key={video.key} 
                                    className={` shadow-md  cursor-pointer rounded-md overflow-hidden transition-colors ${
                                        selectedVideo?.key === video.key ? '' : ' hover:bg-zinc-700/70'
                                    }`}
                                    onClick={() => onSelectVideo(video)}
                                >
                                    <div className="p-2 aspect-video bg-black relative">
                                    </div>
                                    <div className="p-2">
                                        <p className=" text-sm font-medium truncate">
                                            {video.filename || `Recording ${video.key}`}
                                        </p>
                                        <p className=" text-xs mt-1">
                                            {formatDetailedDate(video.lastModified)}
                                        </p>
                                        <p className=" text-xs">
                                            {video.size ? `${(video.size / (1024 * 1024)).toFixed(1)} MB` : ''}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </ScrollArea>
            </div>
        </div>
    );
};
