import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { getIcon } from '@/components/OpportunityGrid/OpportunityCard/OpportunityCard';
import { PageKeys, TPages } from './IdpDashboard';

const OpportunitiesSidebar = ({
  pages,
  onPageChange,
}: {
  pages: TPages;
  onPageChange: (page: PageKeys) => void;
}) => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      const screenWidth = window.innerWidth;
      const threshold = 150; // Distance from the right edge (in pixels)

      if (event.clientX > screenWidth - threshold) {
        setIsOpen(true);
      } else {
        setIsOpen(false);
      }
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <motion.div
      initial={{ x: '100%' }}
      animate={{ x: isOpen ? 0 : '100%' }}
      exit={{ x: '100%' }}
      className="opportunity-sidebar"
    >
      <div>
        {Object.entries(pages).map(([page, isSelected]) => {
          if (page === 'idp-dashboard') return null;
          return (
            <button
              style={{ inset: 'unset', width: '100%' }}
              key={page}
              className={`card ${isSelected ? 'selected' : ''}`}
              onClick={() => onPageChange(page as PageKeys)}
            >
              {getIcon(page, true)}
              <p
                className={`${isSelected ? 'sidebar-item-text-selected' : 'sidebar-item-text'}`}
              >
                {page}
              </p>
            </button>
          );
        })}
      </div>
    </motion.div>
  );
};

export default OpportunitiesSidebar;
