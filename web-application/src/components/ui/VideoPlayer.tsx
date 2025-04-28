import React from 'react';

interface VideoPlayerProps {
  thumbnail: string;
  date: string;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ thumbnail, date }) => {
  return (
    <div className="flex flex-col items-center">
      <div className="w-40 h-24 bg-gray-300 rounded-md mb-2 overflow-hidden">
        <img src={thumbnail} alt="Video thumbnail" className="w-full h-full object-cover" />
      </div>
      {/* Video player */}
      <p className="text-sm">{date}</p>
      <button className="mt-2 px-3 py-1 bg-black text-white rounded text-sm">Download</button>
    </div>
  );
};

export default VideoPlayer;
