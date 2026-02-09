import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, remove it and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// Authentication API functions
export const authAPI = {
  // Login user
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/login', { email, password });
    return response.data;
  },

  // Register user
  register: async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/signup', { email, password });
    return response.data;
  },

  // Get current user info
  getCurrentUser: async () => {
    const response = await apiClient.get('/api/users/me');
    return response.data;
  },
};

// Task API functions
export const taskAPI = {
  // Get user's tasks
  getUserTasks: async (userId: number, completed?: boolean) => {
    const params = completed !== undefined ? { completed } : {};
    const response = await apiClient.get(`/api/${userId}/tasks`, { params });
    return response.data;
  },

  // Create a new task
  createTask: async (userId: number, title: string, description?: string | null) => {
    const response = await apiClient.post(`/api/${userId}/tasks`, { 
      title, 
      description: description || null 
    });
    return response.data;
  },

  // Update a task
  updateTask: async (userId: number, taskId: number, updates: { title?: string; description?: string | null; completed?: boolean }) => {
    const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, updates);
    return response.data;
  },

  // Delete a task
  deleteTask: async (userId: number, taskId: number) => {
    const response = await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Toggle task completion
  toggleTaskCompletion: async (userId: number, taskId: number, completed: boolean) => {
    const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`, { completed });
    return response.data;
  },
};