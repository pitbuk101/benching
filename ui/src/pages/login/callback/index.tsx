'use client';
import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react';

interface LoginCallbackProps {
  children?: React.ReactNode;
}
const LoginCallback: React.FC<LoginCallbackProps> = () => {
  const router = useRouter();
  useEffect(() => {
    router.push('/home');
  });
  return <></>;
};
export default LoginCallback;
