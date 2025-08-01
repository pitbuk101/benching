import GlobeSkeleton from '@/components/Globe/GlobeSkeleton';
import dynamic from 'next/dynamic';
const RotatingEarth = dynamic(() => import('@/components/Globe/Globe'), {
  loading: GlobeSkeleton,
});

interface TotalSavingOpportunityCardProps {
  totalSavings: number;
  currency?: string;
  showGlobe?: boolean;
}

const TotalSavingOpportunityCard: React.FC<TotalSavingOpportunityCardProps> = ({
  totalSavings,
  currency = 'EUR',
  showGlobe = false,
}) => {
  // Format the number with commas as thousand separators
  const formatAmount = (amount: number): string => {
    return amount.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  return (
    <div className="opportunities-card">
      <h2 className="opportunities-title">
        {showGlobe
          ? 'Your Saving Opportunity Around Globe'
          : 'Your Opportunities'}
      </h2>
      <div className="opportunities-content">
        <div className="saving-info">
          <span className="saving-label">Total Saving Opportunity</span>
          <div className="saving-amount">
            <span className="currency">{currency}</span>
            <span className="amount">{formatAmount(totalSavings)}M</span>
          </div>
        </div>
        {showGlobe && (
          <div className="globe-container">
            <RotatingEarth />
          </div>
        )}
      </div>
    </div>
  );
};

export default TotalSavingOpportunityCard;
