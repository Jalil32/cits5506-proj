// pages/HomePage.jsx
import React, { useState } from 'react';
import { VideoSection } from '../components/VideoSection';
import { NotificationPanel } from '../components/NotificationPanel';
import { useVideos } from '../hooks/useVideos';
import type { NotificationData } from '../types';

const HomePage = () => {
    const {
        videos,
        selectedVideo,
        loading,
        error,
        fetchVideos,
        setSelectedVideo,
        handleVideoError,
    } = useVideos();

    const [privacyMode, setPrivacyMode] = useState<boolean>(false);

    const notifications: NotificationData[] = [
        { time: '11:01 AM', message: 'Motion detected in camera 1' },
        { time: '10:45 AM', message: 'Camera 2 went offline' },
        { time: '10:30 AM', message: 'New recording available' },
    ];

	//<NotificationPanel notifications={notifications} />
    return (
        <div className=" h-full flex flex-row">
            <VideoSection
                videos={videos}
                selectedVideo={selectedVideo}
                loading={loading}
                error={error}
                privacyMode={privacyMode}
                onRefresh={fetchVideos}
                onSelectVideo={setSelectedVideo}
                onVideoError={handleVideoError}
                onTogglePrivacy={() => setPrivacyMode(!privacyMode)}
            />
        </div>
    );
};

export default HomePage;
