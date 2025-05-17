import { useState } from 'react';
import { VideoSection } from './components/VideoSection';
import { NotificationPanel } from './components/NotificationPanel';
import { useVideos } from './hooks/useVideos';
import type { NotificationData } from './types';
import './App.css';

const App: React.FC = () => {
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

    return (
        <div className="overflow-hidden h-screen w-screen bg-zinc-950 p-2 md:p-4">
            <div className="h-full flex flex-col lg:flex-row gap-4 max-w-full overflow-hidden">
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

                <NotificationPanel notifications={notifications} />
            </div>
        </div>
    );
};

export default App;
