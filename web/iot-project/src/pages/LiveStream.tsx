import CameraStreamView from "@/components/CameraStreamView";
import PrivacyMode from "@/components/PrivacyMode";

const LiveStreamPage = () => {
    return (
		<div className="flex flex-row">
			<CameraStreamView/>
			<PrivacyMode></PrivacyMode>
		</div>
    );
};

export default LiveStreamPage;
