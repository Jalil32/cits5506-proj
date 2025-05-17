
import CameraStreamView from "@/components/CameraStreamView";
import PrivacyMode from "@/components/PrivacyMode";
		//<h1 className="text-3xl font-bold mb-6">LiveStream</h1>
		//          <div className="bg-gray-800 rounded-lg w-full aspect-video flex items-center justify-center mb-6">
		//              <p className="text-white text-lg">Live Stream Preview</p>
		//          </div>
		//          <div className="flex space-x-4">
		//              <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md">
		//                  Go Live
		//              </button>
		//              <button className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md">
		//                  Settings
		//              </button>
		//          </div>
		//          {/* Add more live stream content here */}
		//      </div>
const LiveStreamPage = () => {
    return (
		<div className="flex flex-row">
			<CameraStreamView/>
			<PrivacyMode></PrivacyMode>
		</div>
    );
};

export default LiveStreamPage;
