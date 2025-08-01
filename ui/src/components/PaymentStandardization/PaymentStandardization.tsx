import dynamic from 'next/dynamic';
import SingleKpi from '../SingleKpiCard/SingleKpi';
import PaymentTablleSkeleton from './subComponents/PaymentTablleSkeleton';
const PaymentTable = dynamic(() => import('./subComponents/PaymentTable'), {
  loading: PaymentTablleSkeleton,
});

const PaymentStandardization = () => {
  return (
    <div className="payment-standardization-container">
      <div className="kpi-grid-container">
        {/* First Row - 6 Equal Columns */}
        <div className="col">
          <SingleKpi title="Total Payments" value="25000000" formate />
        </div>
        <div className="col">
          <SingleKpi title="Payment days weighted" value="123" formate />
        </div>
        <div className="col">
          <SingleKpi title="No. of payment terms" value="39" formate />
        </div>
        <div className="col">
          <SingleKpi title="Standard payment days" value="90" formate />
        </div>
        <div className="col">
          <SingleKpi title="WACC %" value="1" />
        </div>
        <div className="col">
          <SingleKpi
            title="Standardization opportunity"
            value="260000"
            formate
          />
        </div>
      </div>
      <div className="table-grid-container">
        {/* Second Row - Full Width */}
        <div className="col full-width full-height">
          <PaymentTable />
        </div>
      </div>
    </div>
  );
};

export default PaymentStandardization;
