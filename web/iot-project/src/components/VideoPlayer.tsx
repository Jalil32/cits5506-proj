import { CardContent, Card } from './ui/card';
import { Button } from './ui/button';
import { Download, Video } from 'lucide-react';
import { formatDate, formatFileSize } from '../utils/formatters';
import type { VideoData } from '@/types';

interface VideoPlayerProps {
    video: VideoData;
    onClick: () => void;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({ video, onClick }) => {
    return (
        <Card
            className="w-40 bg-zinc-900 border-zinc-800 hover:border-zinc-700 cursor-pointer transition-all"
            onClick={onClick}
        >
            <CardContent className="p-2">
                <div className=" h-24 bg-zinc-800 rounded-md mb-2 relative flex items-center justify-center">
                    <div className="absolute inset-0 bg-black opacity-60 rounded-md flex items-center justify-center">
                        <Video className="w-6 h-6 text-white opacity-70" />
                    </div>
                </div>
                <div className="flex flex-col items-center space-y-2">
                    <span
                        className="text-xs text-zinc-400 truncate  text-center"
                        title={formatDate(video.lastModified)}
                    >
                        {formatDate(video.lastModified)}
                    </span>
                    <span
                        className="text-xs text-zinc-500 truncate  text-center"
                        title={video.filename}
                    >
                        {video.filename}
                    </span>
                    <span className="text-xs text-zinc-600">
                        {formatFileSize(video.size)}
                    </span>
                    <Button
                        variant="secondary"
                        size="sm"
                        className=""
                        onClick={(e) => {
                            e.stopPropagation();
                            window.open(video.url, '_blank');
                        }}
                    >
                        <Download className="w-4 h-4 mr-2" />
                        Download
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
};
