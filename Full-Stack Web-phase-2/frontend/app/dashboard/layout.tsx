'use client';

import { ReactNode } from 'react';
import { useProtectedRoute } from '@/hooks/useProtectedRoute';
import { useRouter } from 'next/navigation';
import { Skeleton } from '@/components/ui/skeleton';

export default function ProtectedLayout({ 
  children 
}: { 
  children: ReactNode 
}) {
  const { isAuthenticated, isLoading } = useProtectedRoute('/login');
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col space-y-3">
          <Skeleton className="h-4 w-[250px]" />
          <Skeleton className="h-4 w-[200px]" />
          <Skeleton className="h-4 w-[250px]" />
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // The hook will handle the redirect
  }

  return (
    <>
      {children}
    </>
  );
}