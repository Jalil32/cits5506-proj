import React from 'react';

interface NotificationProps {
  time: string;
  message: string;
}

const Notification: React.FC<NotificationProps> = ({ time, message }) => {
  return (
    <div className="flex flex-col mb-4">
        {/* Time - update later*/}
      <span className="text-xs text-gray-500">{time}</span>
      <div className="bg-white rounded px-3 py-2 shadow-sm">
        {/* Message - update later */}

      </div>
    </div>
  );
};

export default Notification;
