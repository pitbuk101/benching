import { motion, AnimatePresence } from 'framer-motion';
import OpportunityCard from './OpportunityCard/OpportunityCard'; // { getIcon }
import { useState } from 'react';
import { PageKeys } from '@/pages/idp-dashboard/IdpDashboard';

const OpportunitiesGrid = ({
  onPageChange,
}: {
  onPageChange: (page: PageKeys) => void;
}) => {
  const [selectedCardId, setSelectedCardId] = useState(null);

  const opportunities = [
    {
      id: 1,
      title: 'Payment Terms Standardization',
      amount: 'USD 9.7M',
      insights: 4,
      isNew: 0,
    },
    {
      id: 2,
      title: 'Rates Harmonization',
      amount: 'USD 2.4M',
      insights: 4,
      isNew: 2,
    },
    {
      id: 3,
      title: 'Parametric Cost Modeling',
      amount: 'USD 1.2M',
      insights: 4,
      isNew: 2,
    },
    { id: 4, title: 'OEM non-OEM', amount: 'USD 1.0M', insights: 4, isNew: 2 },
    {
      id: 5,
      title: 'Early Payments',
      amount: 'USD 1.0M',
      insights: 4,
      isNew: 0,
    },
    {
      id: 6,
      title: 'Unused Discounts',
      amount: 'USD 21.7K',
      insights: 4,
      isNew: 2,
    },
    {
      id: 7,
      title: 'Payment Terms Standardization',
      amount: 'USD 9.7M',
      insights: 4,
      isNew: 0,
    },
    {
      id: 8,
      title: 'Rates Harmonization2',
      amount: 'USD 2.4M',
      insights: 4,
      isNew: 2,
    },
    {
      id: 9,
      title: 'Parametric Cost Modeling2',
      amount: 'USD 1.2M',
      insights: 4,
      isNew: 2,
    },
  ];

  const handleCardClick = (data: (typeof opportunities)[0]) => {
    setSelectedCardId(data.id);
    onPageChange(data.title as PageKeys);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        when: 'beforeChildren',
        staggerChildren: 0.1,
      },
    },
    exit: {
      opacity: 0,
      transition: {
        when: 'afterChildren',
        staggerChildren: 0.05,
        staggerDirection: -1,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.3 },
    },
    exit: (id) => ({
      x: window.innerWidth,
      opacity: 0,
      transition: {
        duration: 0.5,
        delay:
          selectedCardId === id ? 0 : 0.1 * Math.abs(selectedCardId - id) * 0.1,
      },
    }),
  };

  return (
    <div style={{ width: '100%', position: 'relative' }}>
      <AnimatePresence mode="wait">
        <motion.div
          className="opportunities-container"
          key="grid"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
        >
          <h3 className="opportunities-title">Identified Opportunities</h3>
          <div className="opportunityCard_grid">
            {opportunities.map((opportunity) => (
              <motion.div
                key={opportunity.id}
                variants={cardVariants}
                custom={opportunity.id}
                onClick={() => handleCardClick(opportunity)}
                className="cursor-pointer"
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.98 }}
              >
                <OpportunityCard {...opportunity} />
              </motion.div>
            ))}
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default OpportunitiesGrid;
