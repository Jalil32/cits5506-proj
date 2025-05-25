function CameraStreamView() {
  return (
    <div className=" w-1/2 h-full" >
      <iframe
        src="http://192.168.0.44:8080/"
        title="Security Camera"
		className="w-full h-full"
      />
    </div>
  );
}

export default CameraStreamView
