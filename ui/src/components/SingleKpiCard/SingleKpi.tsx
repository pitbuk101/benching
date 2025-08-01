import { ExternalLink } from 'lucide-react';
import Link from 'next/link';
import { formatNumber } from '@/utils/utils';
import useCount from '@/hooks/useCountUp';

interface SingleKPICardProps {
  title: string;
  value: string;
  path?: string;
  formate?: boolean;
}

const SingleKpi = ({
  title,
  value,
  path,
  formate = false,
}: SingleKPICardProps) => {
  const formattedValue = formate ? formatNumber(value) : value;
  const animatedValue =
    useCount(parseFloat(formattedValue.slice(0, -1))) +
    formattedValue.slice(-1);

  return (
    <div className="single-kpi-card">
      <div className="single-kpi-header">
        <h2 className={'single-kpi-title idp-kpi-title'}>{title}</h2>
        {path && (
          <Link className="single-kpi-link" href={path}>
            <ExternalLink size={15} className="cursor-pointer text-black" />
          </Link>
        )}
      </div>

      <p className="single-kpi-value">{animatedValue}</p>
    </div>
  );
};

export default SingleKpi;
