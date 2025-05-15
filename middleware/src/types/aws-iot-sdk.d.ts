declare module "aws-iot-device-sdk" {
	interface DeviceOptions {
		keyPath: string;
		certPath: string;
		caPath: string;
		clientId: string;
		host: string;
		keepalive?: number;
		protocol?: string;
		port?: number;
		debug?: boolean;
	}

	interface PublishOptions {
		qos: number;
		retain?: boolean;
	}

	class Device {
		constructor(options: DeviceOptions);
		on(event: string, callback: (...args: any[]) => void): this;
		end(force?: boolean, callback?: () => void): void;
		publish(
			topic: string,
			message: string,
			options: PublishOptions,
			callback?: (error?: Error) => void,
		): void;
		subscribe(
			topic: string,
			options?: object,
			callback?: (error?: Error, granted?: any) => void,
		): void;
		unsubscribe(
			topic: string,
			options?: object,
			callback?: (error?: Error) => void,
		): void;
	}

	// Define a function that returns a Device instance
	function device(options: DeviceOptions): Device;

	export { device, DeviceOptions, Device };
}
