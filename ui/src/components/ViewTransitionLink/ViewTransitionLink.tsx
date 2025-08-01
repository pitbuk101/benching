import { MouseEvent, ReactNode } from 'react';
import { useRouter } from 'next/router';
import { isServer } from '@/utils/helper';

const ViewTransitionLink = ({
  to = '#',
  children,
  className,
}: {
  to?: string;
  children?: ReactNode;
  className?: string;
}) => {
  const router = useRouter();

  const navigate = async (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    if (!to || isServer()) return;
    (document as any).startViewTransition(() => {
      router.push(to);
    });
  };

  const prop = className ? { className } : {};

  return (
    <button
      style={{ inset: 'unset', width: '100%' }}
      {...prop}
      onClick={navigate}
    >
      {children}
    </button>
  );
};

export default ViewTransitionLink;
