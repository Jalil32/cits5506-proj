import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';
import { toast } from 'sonner';

// Types
export interface Notification {
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timestamp: string;
  deviceId?: string;
  metadata?: Record<string, any>;
}

export interface PrivacyStatus {
  privacyModeEnabled: boolean;
  deviceId: string;
  lastStateChange: string;
  isRecording: boolean;
}

interface NotificationContextType {
  isConnected: boolean;
  privacyStatus: PrivacyStatus | null;
  setPrivacyMode: (enabled: boolean) => Promise<void>;
}

// Create context
const NotificationContext = createContext<NotificationContextType>({
  isConnected: false,
  privacyStatus: null,
  setPrivacyMode: async () => {},
});

// Socket.IO instance
// Use the same port as your Express server
const SOCKET_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';
let socket: Socket;

export const NotificationProvider = ({ children }: { children: ReactNode }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [privacyStatus, setPrivacyStatus] = useState<PrivacyStatus | null>(null);

  useEffect(() => {
    // Initialize socket connection
    socket = io(SOCKET_URL);

    // Connection event handlers
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
      setIsConnected(false);
    });

    // Listen for notifications
    socket.on('camera-notification', (notification: Notification) => {
      console.log('Received notification:', notification);
      
      // Dsplay toast notification based on the type
      switch (notification.type) {
        case 'success':
          toast.success(notification.message);
          break;
        case 'error':
          toast.error(notification.message);
          break;
        case 'warning':
          toast.warning(notification.message);
          break;
        default:
          toast.info(notification.message);
      }
    });

    // Listen for privacy status updates
    socket.on('privacy-status', (status: PrivacyStatus) => {
      console.log('Received privacy status update:', status);
      setPrivacyStatus(status);
    });

    // Clean up on unmount
    return () => {
      socket.disconnect();
    };
  }, []);

  // Function to set privacy mode via API
  const setPrivacyMode = async (enabled: boolean): Promise<void> => {
    try {
      const response = await fetch(`${SOCKET_URL}/api/privacy-mode`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ enabled }),
      });

      if (!response.ok) {
        throw new Error('Failed to set privacy mode');
      }
    } catch (error) {
      console.error('Error setting privacy mode:', error);
      toast.error('Failed to set privacy mode. Please try again.');
      throw error;
    }
  };

  return (
    <NotificationContext.Provider
      value={{
        isConnected,
        privacyStatus,
        setPrivacyMode,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};

// Custom hook for using the notification context
export const useNotifications = () => useContext(NotificationContext);
