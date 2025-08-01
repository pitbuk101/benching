export function formatNumber(value: number | string, decimals: number = 2) {
  if (typeof value !== 'number') value = Number(value);
  if (isNaN(value)) return 'Invalid number';

  const formatter = new Intl.NumberFormat('en', {
    notation: 'compact',
    maximumFractionDigits: decimals,
  });

  return formatter.format(value);
}

export const formatNumberWithCommas = ({
  value,
  locale = 'en-US',
  decimal = 2,
}: {
  value: number | string;
  locale?: string;
  decimal?: number;
}): string => {
  // for location support give set local = navigator.language
  if (!value) return '-';

  return new Intl.NumberFormat(locale, {
    maximumFractionDigits: decimal,
  }).format(Number(value));
};
