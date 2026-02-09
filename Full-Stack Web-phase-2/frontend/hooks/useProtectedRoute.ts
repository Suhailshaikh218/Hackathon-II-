import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export function useProtectedRoute(redirectUrl: string = '/login') {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectUrl);
    }
  }, [isAuthenticated, isLoading, router, redirectUrl]);

  return { isAuthenticated, isLoading };
}