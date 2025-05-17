// src/components/VideoGallery.tsx
import type React from 'react';
import { VideoPlayer } from './VideoPlayer';
import type { VideoData } from '../types';
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
} from '@/components/ui/carousel';
import { Card, CardContent } from './ui/card';

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
        <Carousel className="w-full max-w-sm">
            <CarouselContent className="-ml-1">
                {Array.from({ length: 5 }).map((_, index) => (
                    <CarouselItem
                        key={index}
                        className="pl-1 md:basis-1/2 lg:basis-1/3"
                    >
                        <div className="p-1">
                            <Card>
                                <CardContent className="flex aspect-square items-center justify-center p-6">
                                    <span className="text-2xl font-semibold">
                                        {index + 1}
                                    </span>
                                </CardContent>
                            </Card>
                        </div>
                    </CarouselItem>
                ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
        </Carousel>
    );
};
