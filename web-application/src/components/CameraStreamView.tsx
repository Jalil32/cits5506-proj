function CameraStreamView() {
  return (
    <div className="camera-stream-container">
      <iframe
        src="http://172.20.10.11:8080/"
        title="Security Camera"
        width="840"
        height="680"
        style={{ border: 'none', borderRadius: '8px' }}
      />
    </div>
  );
}

export default CameraStreamView
