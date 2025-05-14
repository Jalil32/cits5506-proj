import React from 'react';
import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { ScrollArea } from "./components/ui/scroll-area";
import { Bell, Download, Maximize2, Video } from "lucide-react";
import './App.css';

// 创建临时的 VideoPlayer 组件
const VideoPlayer: React.FC<{ thumbnail?: string; date?: string }> = ({ thumbnail, date }) => {
  return (
    <Card className="w-40 bg-zinc-900 border-zinc-800">
      <CardContent className="p-2">
        <div className="w-full h-24 bg-zinc-800 rounded-md mb-2"></div>
        <div className="flex flex-col items-center space-y-2">
          <span className="text-xs text-zinc-400">{date || 'No date'}</span>
          <Button variant="secondary" size="sm" className="w-full">
            <Download className="w-4 h-4 mr-2" />
            Download
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

// 创建临时的 Notification 组件
const Notification: React.FC<{ time?: string; message?: string }> = ({ time, message }) => {
  return (
    <Card className="mb-2 bg-zinc-900 border-zinc-800">
      <CardContent className="p-3">
        <div className="flex flex-col space-y-1">
          <span className="text-xs text-zinc-400">{time || 'No time'}</span>
          <p className="text-sm text-zinc-100">{message || 'No message'}</p>
        </div>
      </CardContent>
    </Card>
  );
};

const App: React.FC = () => {
  // 添加示例数据
  const videos = [
    { thumbnail: '', date: '2025-04-24 08:00 AM' },
    { thumbnail: '', date: '2025-04-24 09:00 AM' },
    { thumbnail: '', date: '2025-04-24 10:00 AM' },
  ];

  const notifications = [
    { time: '11:01 AM', message: 'Motion detected in camera 1' },
    { time: '10:45 AM', message: 'Camera 2 went offline' },
    { time: '10:30 AM', message: 'New recording available' },
  ];

  return (
    <div className="min-h-screen w-full bg-zinc-950 p-4">
      <div className="flex flex-col md:flex-row gap-4">
        {/* Left part: Livestream video and controls */}
        <Card className="flex-1 bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-100">Home Security Monitoring</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Live Video Block */}
            <div className="relative bg-zinc-800 h-80 rounded-lg">
              <Badge variant="secondary" className="absolute top-2 left-2 bg-zinc-700">
                <div className="w-2 h-2 bg-red-500 rounded-full mr-1"></div>
                LIVE
              </Badge>
              <Button variant="ghost" size="icon" className="absolute top-2 right-2 text-zinc-100 hover:bg-zinc-700">
                <Maximize2 className="h-4 w-4" />
              </Button>
            </div>

            {/* Privacy Mode Button */}
            <div className="flex justify-end">
              <Button variant="destructive">Privacy Mode ON</Button>
            </div>

            {/* Video Shortcut Section */}
            <div>
              <h3 className="font-semibold mb-4 text-zinc-100">Detected Video Shortcuts</h3>
              <ScrollArea className="w-full">
                <div className="flex items-center space-x-4">
                  <Button variant="ghost" size="icon" className="text-zinc-100 hover:bg-zinc-700">
                    <Video className="h-4 w-4 rotate-180" />
                  </Button>
                  <div className="flex gap-4">
                    {videos.map((video, index) => (
                      <VideoPlayer
                        key={index}
                        thumbnail={video.thumbnail}
                        date={video.date}
                      />
                    ))}
                  </div>
                  <Button variant="ghost" size="icon" className="text-zinc-100 hover:bg-zinc-700">
                    <Video className="h-4 w-4" />
                  </Button>
                </div>
              </ScrollArea>
            </div>
          </CardContent>
        </Card>

        {/* Right part: Notification Panel */}
        <Card className="w-full md:w-80 bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="flex items-center text-zinc-100">
              <Bell className="h-4 w-4 mr-2" />
              Notifications
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-[calc(100vh-12rem)]">
              {notifications.map((note, index) => (
                <Notification
                  key={index}
                  time={note.time}
                  message={note.message}
                />
              ))}
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default App;
