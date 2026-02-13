import { API_CONFIG } from '../config/api';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  history?: Message[];
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  history: Message[];
}

export const chatApi = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_CONFIG.BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error('发送消息失败');
    }

    return response.json();
  },

  async clearHistory(sessionId: string = 'default'): Promise<void> {
    const response = await fetch(`${API_CONFIG.BASE_URL}/clear?session_id=${sessionId}`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error('清除历史失败');
    }
  },

  async healthCheck(): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_CONFIG.BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error('健康检查失败');
    }

    return response.json();
  },
};
