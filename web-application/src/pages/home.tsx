import  { useState } from 'react';
import { VideoSection } from '../components/VideoSection';
import { useVideos } from '../hooks/useVideos';

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
