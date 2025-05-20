export interface VideoData {
	key: string;
	filename: string;
	size: number;
	lastModified: Date;
	url: string;
	thumbnailUrl?: string;
}

export interface NotificationData {
	time: string;
	message: string;
}
