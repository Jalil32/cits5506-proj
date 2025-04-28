import * as React from "react"
import { cn } from "@/lib/utils"
import React from 'react';
import { Button } from './button';
import VideoPlayer from './VideoPlayer';
import Notification from './Notification';

const Livestream: React.FC = () => {
  const videos = [
    // fake link
    {
      thumbnail: 'https://.com',
      date: '2025-01-01'
    },

  ];

  const notifications = [
    // fake message
    {
      time: '2025-01-01',
      message: 'Notification 1'
    },
    {
      time: '2025-01-02',
      message: 'Notification 2'
    }
  ];

  return (
    <div className="flex h-screen">
      {/* Main Live View */}
      <div className="flex-1 flex flex-col p-4">
        {/* Live Video */}
        <div className="relative bg-gray-300 h-80 rounded-md">
          <div className="absolute top-2 left-2 flex items-center bg-gray-600 text-white text-xs rounded-full px-2 py-1">
            <div className="w-2 h-2 bg-red-500 rounded-full mr-1"></div>
            LIVE
          </div>
          <div className="absolute top-2 right-2 bg-white p-1 rounded-full cursor-pointer">
            ⛶ {/* fullscreen icon placeholder */}
          </div>
        </div>

        {/* Privacy Mode Button */}
        <div className="flex justify-end mt-2">
          <Button label="Privacy Mode ON" className="bg-red-500 text-white" />
        </div>

        {/* Video Shortcut */}
        <div className="mt-6">
          <h3 className="font-bold mb-4">Video shortcut</h3>
          <div className="flex items-center">
            <button className="text-2xl mr-2"></button>
            <div className="flex gap-4">
              {videos.map((video) => (
                <VideoPlayer
                  thumbnail={video.thumbnail}
                  date={video.date}
                />
              ))}
            </div>
            <button className="text-2xl ml-2">➡️</button>
          </div>
        </div>
      </div>

      {/* Notification Panel */}
      <div className="w-80 bg-gray-100 p-4 border-l overflow-y-auto">
        <h3 className="font-bold mb-4">Notifications</h3>
        {notifications.map((note, index) => (
          <Notification
            key={index}
            time={note.time}
            message={note.message}
          />
        ))}
      </div>
    </div>
  );
};

export default Livestream;
