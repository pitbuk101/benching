import { useState } from 'react';
import dynamic from 'next/dynamic';
import SingleKpi from '@/components/SingleKpiCard/SingleKpi';
import OpportunitiesGrid from '@/components/OpportunityGrid/OpportunityGrid';
const SwitchableBarChart = dynamic(
  () => import('@/components/SwitchBarChart/SwitchBarChart'),
);
import 'ag-charts-enterprise';
import TotalSavingOpportunityCard from '@/components/OpportunityGrid/TotatSavingOpportunity/TotalSavingOpportunityCard';
import PaymentStandardization from '@/components/PaymentStandardization/PaymentStandardization';
import RightFadeIn from '@/components/RightFadeIn/RightFadeIn';
import { ChevronLeft } from 'lucide-react';
import Sidebar from './OpportunitiesSidebar';

const initialPages = {
  'idp-dashboard': true,
  'Payment Terms Standardization': false,
  'Rates Harmonization': false,
  'Parametric Cost Modeling': false,
  'OEM non-OEM': false,
  'Early Payments': false,
  'Unused Discounts': false,
  'Rates Harmonization2': false,
  'Parametric Cost Modeling2': false,
};

export type TPages = typeof initialPages;
export type PageKeys = keyof typeof initialPages;

const IDPDashboard = () => {
  const [pages, setPages] = useState<TPages>(initialPages);

  const onPageChange = (page: PageKeys) => {
    setTimeout(() => {
      setPages(
        (prev) =>
          Object.fromEntries(
            Object.keys(prev).map((key) => [key, key === page]),
          ) as typeof initialPages,
      );
    }, 500);
  };

  return (
    <>
      {pages['idp-dashboard'] && (
        <RightFadeIn>
          <div className="idp-dashboard">
            <div className="idp-kpi-grid">
              <div className="idp-kpi-item">
                <SingleKpi title="Spend" value="123000" formate />
              </div>
              <div className="idp-kpi-item">
                <SingleKpi title="No. of suppliers" value="2050000" formate />
              </div>
              <div className="idp-kpi-item">
                <SingleKpi title="Opportunities %" value="13.7%" />
              </div>
              <div className="idp-kpi-item">
                <SingleKpi title="Opportunity" value="60300" formate />
              </div>
            </div>

            <div className="idp-charts-grid">
              <TotalSavingOpportunityCard
                totalSavings={29.71}
                currency="USD"
                showGlobe
              />
              <SwitchableBarChart />
            </div>
            <div className="idp-opportunities-grid">
              <OpportunitiesGrid onPageChange={onPageChange} />
            </div>
          </div>
        </RightFadeIn>
      )}
      <>
        {!pages['idp-dashboard'] && (
          <Sidebar pages={pages} onPageChange={onPageChange} />
        )}

        {pages['Payment Terms Standardization'] && (
          <RightFadeIn>
            <div className="max_space page_container">
              <button
                style={{ inset: 'unset' }}
                className="page_container_header"
                onClick={() => onPageChange('idp-dashboard')}
              >
                <ChevronLeft className="page_container_icon" />
                Payment Terms Standardization
              </button>
              <PaymentStandardization />
            </div>
          </RightFadeIn>
        )}
      </>
    </>
  );
};

export default IDPDashboard;
