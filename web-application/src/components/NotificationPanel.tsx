// src/components/NotificationPanel.tsx
import type React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { ScrollArea } from "./ui/scroll-area";
import { Bell } from "lucide-react";
import { NotificationItem } from "./NotificationItem";
import type { NotificationData } from "../types";

interface NotificationPanelProps {
	notifications: NotificationData[];
}

export const NotificationPanel: React.FC<NotificationPanelProps> = ({
	notifications,
}) => {
	return (
		<Card className="w-full lg:w-80 bg-zinc-900 border-zinc-800 shrink-0">
			<CardHeader>
				<CardTitle className="flex items-center text-zinc-100">
					<Bell className="h-4 w-4 mr-2" />
					Notifications
				</CardTitle>
			</CardHeader>
			<CardContent>
				<ScrollArea className="h-[60vh] md:h-[70vh] lg:h-[calc(100vh-12rem)]">
					{notifications.length === 0 ? (
						<div className="flex items-center justify-center h-24 w-full">
							<p className="text-zinc-400">No notifications</p>
						</div>
					) : (
						notifications.map((notification, index) => (
							<NotificationItem key={index} notification={notification} />
						))
					)}
				</ScrollArea>
			</CardContent>
		</Card>
	);
};
