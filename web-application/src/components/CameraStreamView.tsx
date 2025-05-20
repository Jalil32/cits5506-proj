function CameraStreamView() {
  return (
    <div className=" w-1/2 h-full" >
      <iframe
        src="http://172.20.10.11:8080/"
        title="Security Camera"
		className="w-full h-full"
      />
    </div>
  );
}

export default CameraStreamView
