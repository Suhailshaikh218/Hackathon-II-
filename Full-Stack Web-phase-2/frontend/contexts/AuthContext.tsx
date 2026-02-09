'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '@/lib/api';

interface User {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    const storedToken = localStorage.getItem('access_token');
    
    if (storedToken) {
      try {
        // Attempt to get user info to verify token validity
        const userData = await authAPI.getCurrentUser();
        setUser(userData);
        setToken(storedToken);
      } catch (error) {
        // Token is invalid or expired, remove it
        localStorage.removeItem('access_token');
      }
    }
    
    setIsLoading(false);
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      
      if (response.access_token) {
        const { access_token, user } = response;
        
        localStorage.setItem('access_token', access_token);
        setToken(access_token);
        setUser(user);
      } else {
        throw new Error('Login failed: No token received');
      }
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await authAPI.register(email, password);
      
      if (response.id) {
        // Auto-login after registration
        await login(email, password);
      } else {
        throw new Error('Registration failed');
      }
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setToken(null);
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isLoading,
    login,
    register,
    logout,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}