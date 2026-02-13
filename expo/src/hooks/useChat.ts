import { useState } from 'react';
import { chatApi, Message } from '../api/chatApi';

export const useChat = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (message: string, sessionId: string = 'default') => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage({
        message,
        session_id: sessionId,
      });
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '发送消息失败';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = async (sessionId: string = 'default') => {
    setIsLoading(true);
    setError(null);

    try {
      await chatApi.clearHistory(sessionId);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '清除历史失败';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    sendMessage,
    clearHistory,
    isLoading,
    error,
  };
};
