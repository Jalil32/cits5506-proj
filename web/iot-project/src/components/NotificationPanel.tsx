// src/components/NotificationPanel.tsx
import type React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { ScrollArea } from './ui/scroll-area';
import { Bell } from 'lucide-react';
import { NotificationItem } from './NotificationItem';
import type { NotificationData } from '../types';

interface NotificationPanelProps {
    notifications: NotificationData[];
}

export const NotificationPanel: React.FC<NotificationPanelProps> = ({
    notifications,
}) => {
    return (
        <div className="pl-4  pt-4  lg:w-80  shrink-0">
            <div className='pb-4'>
                <CardTitle className="w-full  flex items-center ">
                    <Bell className="h-4 w-4 mr-2" />
                    Notifications
                </CardTitle>
            </div>
            <div>
                <ScrollArea className="h-[60vh] md:h-[70vh] lg:h-[calc(100vh-12rem)]">
                    {notifications.length === 0 ? (
                        <div className="flex items-center justify-center h-24 ">
                            <p className="">No notifications</p>
                        </div>
                    ) : (
                        notifications.map((notification, index) => (
                            <NotificationItem
                                key={index}
                                notification={notification}
                            />
                        ))
                    )}
                </ScrollArea>
            </div>
        </div>
    );
};
