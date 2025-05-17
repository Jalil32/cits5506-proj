import type React from "react";
import { Card, CardContent } from "./ui/card";
import type { NotificationData } from "../types";

interface NotificationItemProps {
	notification: NotificationData;
}

export const NotificationItem: React.FC<NotificationItemProps> = ({
	notification,
}) => {
	return (
		<Card className="mb-2 bg-zinc-900 border-zinc-800">
			<CardContent className="p-3">
				<div className="flex flex-col space-y-1">
					<span className="text-xs text-zinc-400">
						{notification.time || "No time"}
					</span>
					<p className="text-sm text-zinc-100">
						{notification.message || "No message"}
					</p>
				</div>
			</CardContent>
		</Card>
	);
};
