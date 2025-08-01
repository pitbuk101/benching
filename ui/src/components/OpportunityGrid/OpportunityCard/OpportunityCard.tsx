import Image from 'next/image';
import React from 'react';

const ICON_MAP = {
  'Payment Terms Standardization': 'payment-term-standarization.svg',
  'Unused Discounts': 'payment-term-standarization.svg',
  'Rates Harmonization': 'rate-harmonisation.svg',
  'Rates Harmonization2': 'rate-harmonisation-2.svg',
  'OEM non-OEM': 'oem-non-oem.svg',
  'Parametric Cost Modeling': 'parametric-cost-modelling.svg',
  'Parametric Cost Modeling2': 'parametric-cost-modelling-2.svg',
  'Early Payments': 'early-payment.svg',
};

export const getIcon = (title, isSideBar = false) => {
  const iconFile = ICON_MAP[title];

  if (!iconFile) {
    return null; // Return nothing if title not found in the map
  }

  const iconPath = `/images/IdentifiedOpportunities/${iconFile}`;

  return (
    <div className="icon-container">
      <Image
        src={iconPath}
        alt={title}
        className={isSideBar ? 'sidebar-icon' : 'card-icon'}
        height={20}
        width={20}
        fill={false}
      />
    </div>
  );
};
const OpportunityCard = ({ title, amount, insights, isNew }) => {
  return (
    <div className="opportunity-card">
      <div className="card-header">
        {getIcon(title)}
        <div className="card-info">
          <div className="card-title">{title}</div>
          <div className="card-amount">{amount}</div>
        </div>
      </div>
      <div className="card-footer">
        <div className="card-insights">{insights} Insights</div>
        {isNew ? <div className="card-new">{isNew} New</div> : null}
      </div>
    </div>
  );
};

export default OpportunityCard;
