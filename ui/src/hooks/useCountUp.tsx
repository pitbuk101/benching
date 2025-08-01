import { useCountUp } from 'use-count-up';

const useCount = (end: number) => {
  const { value } = useCountUp({
    isCounting: true,
    end: end,
    duration: 3.2,
  });

  if (end < 10) return end;
  return value;
};

export default useCount;
