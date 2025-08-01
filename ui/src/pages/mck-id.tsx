'use client';
/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unnecessary-condition */
import type { Mid } from '@mid/sdk';
import { ERROR_MSG } from '@mid/sdk';
import { useRouter } from 'next/navigation';
import { useEffect, useState, useCallback, createContext } from 'react';
import AuthLoader from './loader/auth-loader';

interface McKIdProps {
  mid: Mid;
  children?: React.ReactNode;
  mockedIsAuthed?: any;
  mockLoadFlag?: any;
}

export const AuthContext = createContext({
  isAuthed: null,
  isLoading: null,
});

export const MckId: React.FC<McKIdProps> = ({
  mid,
  children,
  mockedIsAuthed,
  mockLoadFlag,
}: McKIdProps) => {
  const router = useRouter();
  const [isAuthed, setIsAuthed] = useState(mockedIsAuthed || false);
  const [isLoading, setIsLoading] = useState(mockLoadFlag || true);
  const errorMsg = mid?.core?.state.get(ERROR_MSG);

  const checkIsAuth = useCallback(() => {
    mid.isAuthed().then((isAuth) => {
      if (isAuth) {
        setIsAuthed(true);
        setIsLoading(false);
      }
    });
  }, []);

  const login = useCallback(() => {
    mid.login().finally(() => {
      checkIsAuth();
    });
  }, [checkIsAuth]);

  useEffect(() => {
    login();
  }, [login]);

  const redirectToError = () => {
    router.push('/unauthorized');
    return null;
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthed,
        isLoading,
      }}
    >
      {isLoading ? (
        <AuthLoader isLoading={isLoading} errorMsg={errorMsg} size={50} />
      ) : isAuthed ? (
        children
      ) : (
        redirectToError()
      )}
    </AuthContext.Provider>
  );
};

export default MckId;
