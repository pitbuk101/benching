import { useLayoutEffect, useMemo, useState } from 'react';

import type { ColDef } from 'ag-grid-community';
import {
  AllCommunityModule,
  ModuleRegistry,
  ClientSideRowModelModule,
  themeQuartz,
} from 'ag-grid-community';
import { AgGridReact } from 'ag-grid-react';
import {
  AllEnterpriseModule,
  IntegratedChartsModule,
} from 'ag-grid-enterprise';
import { formatNumberWithCommas } from '@/utils/utils';
import PaymentTablleSkeleton from './PaymentTablleSkeleton';

const PaymentTermsTable = () => {
  const [showGrid, setshowGrid] = useState(false);
  useLayoutEffect(() => {
    const script = document.createElement('script');
    script.src =
      'https://cdn.jsdelivr.net/npm/ag-charts-enterprise@11.1.0/dist/umd/ag-charts-enterprise.min.js';
    script.async = true;
    script.onload = () => {
      if ((window as any)?.agCharts?.AgChartsEnterpriseModule) {
        ModuleRegistry.registerModules([
          AllCommunityModule,
          AllEnterpriseModule,
          ClientSideRowModelModule,
          IntegratedChartsModule.with(
            (window as any)?.agCharts?.AgChartsEnterpriseModule,
          ),
        ]);
        setshowGrid(true);
        console.log('AgChartsEnterpriseModule registered successfully!');
      } else {
        console.error('AgChartsEnterpriseModule failed to load.');
      }
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const [rowData] = useState([
    {
      id: 'company1',
      company: 'Pardalis Holding',
      level: 0,
      spend: 24629514.61,
      paymentDaysWeighted: 52,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 249962.12,
      discountPossible: 67792.0,
    },
    {
      id: 'term1',
      company: '30 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 6521035.34,
      paymentDaysWeighted: 44,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 83402.93,
      discountPossible: 0.0,
    },
    {
      id: 'term2',
      company: '0 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 7263081.04,
      paymentDaysWeighted: 61,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 58627.73,
      discountPossible: 0.0,
    },
    {
      id: 'term3',
      company: 'Day 31 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 4538105.79,
      paymentDaysWeighted: 68,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 39752.23,
      discountPossible: 0.0,
    },
    {
      id: 'term4',
      company: '14 (3%) - 30 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 1348640.72,
      paymentDaysWeighted: 17,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 21961.36,
      discountPossible: 41617.24,
    },
    {
      id: 'term5',
      company: '14 (1%) - 30 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 1323097.44,
      paymentDaysWeighted: 21,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 19189.47,
      discountPossible: 13304.58,
    },
    {
      id: 'term6',
      company: '60 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 1545076.5,
      paymentDaysWeighted: 59,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 10978.59,
      discountPossible: 0.0,
    },
    {
      id: 'term7',
      company: '45 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 423759.62,
      paymentDaysWeighted: 39,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 4844.25,
      discountPossible: 0.0,
    },
    {
      id: 'term8',
      company: '1 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 571720.84,
      paymentDaysWeighted: 65,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 3883.18,
      discountPossible: 0.0,
    },
    {
      id: 'term9',
      company: '30 (3%) - 60 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 401930.18,
      paymentDaysWeighted: 32,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 3303.54,
      discountPossible: 12430.82,
    },
    {
      id: 'term10',
      company: '+1 Month(s) Day 31 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 301063.82,
      paymentDaysWeighted: 65,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 2176.29,
      discountPossible: 0.0,
    },
    {
      id: 'term11',
      company: '28 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 58197.91,
      paymentDaysWeighted: 28,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 988.57,
      discountPossible: 0.0,
    },
    {
      id: 'term12',
      company: '+2 Month(s) Day 15 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 57474.58,
      paymentDaysWeighted: 64,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 407.09,
      discountPossible: 0.0,
    },
    {
      id: 'term13',
      company: '14 (1%) - 60 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 24430.57,
      paymentDaysWeighted: 33,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 200.8,
      discountPossible: 244.3,
    },
    {
      id: 'term14',
      company: '15 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 4604.36,
      paymentDaysWeighted: 39,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 64.38,
      discountPossible: 0.0,
    },
    {
      id: 'term15',
      company: '14 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 2889.69,
      paymentDaysWeighted: 19,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 56.21,
      discountPossible: 0.0,
    },
    {
      id: 'term16',
      company: '10 (2%) - 60 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 7395.81,
      paymentDaysWeighted: 50,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 52.36,
      discountPossible: 148.75,
    },
    {
      id: 'term17',
      company: '+3 Month(s) Day 10 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 234732.18,
      paymentDaysWeighted: 96,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 35.11,
      discountPossible: 0.0,
    },
    {
      id: 'term18',
      company: '10 (2%) - 30 (Net)',
      level: 1,
      parentId: 'company1',
      spend: 1322.79,
      paymentDaysWeighted: 8,
      desiredPaymentTermDays: 90,
      waccPercentage: 10.0,
      potentialSavingsByStandardization: 21.74,
      discountPossible: 26.86,
    },
  ]);

  const totalRow = rowData.reduce(
    (acc, row) => ({
      company: 'Total',
      spend: acc?.spend + row?.spend,
      potentialSavingsByStandardization:
        acc?.potentialSavingsByStandardization +
        row?.potentialSavingsByStandardization,
    }),
    {
      spend: 0,
      potentialSavingsByStandardization: 0,
    },
  );

  const { minSpend, maxSpend } = useMemo(() => {
    const minSpend = Math.min(...rowData.map((row) => row.spend));
    const maxSpend = Math.max(...rowData.map((row) => row.spend));
    return { minSpend, maxSpend };
  }, [rowData]);

  const getSpendCellStyle = (params: any) => {
    if (params.node.rowPinned) {
      return { fontWeight: 'bold', textAlign: 'right' };
    }

    const spendValue = params.value;
    const percentage = ((spendValue - minSpend) / (maxSpend - minSpend)) * 100;

    return {
      background: `linear-gradient(to right, #1666ff ${percentage}%, transparent ${percentage}%)`,
      textAlign: 'right',
      paddingRight: '10px',
    };
  };

  const [colDefs] = useState<ColDef[]>([
    {
      field: 'company',
      headerName: 'Company level 1',
      cellRenderer: 'agGroupCellRenderer',
      cellRendererParams: {
        suppressCount: true,
      },
    },
    {
      field: 'spend',
      headerName: 'Spend',
      valueFormatter: (params) =>
        params.value
          ? formatNumberWithCommas({ value: params?.value as number })
          : '',
      cellStyle: getSpendCellStyle,
    },
    {
      field: 'paymentDaysWeighted',
      headerName: 'Payment days weighted',
      width: 150,
    },
    {
      field: 'desiredPaymentTermDays',
      headerName: 'Desired payment term days',
      width: 150,
    },
    {
      field: 'waccPercentage',
      headerName: 'WACC, %',
      valueFormatter: (params) =>
        params?.value ? Number(params?.value)?.toFixed(1) + ' %' : '',
    },
    {
      field: 'potentialSavingsByStandardization',
      headerName: 'Potential savings by standardization',
      width: 200,
      valueFormatter: (params) =>
        params.value
          ? formatNumberWithCommas({ value: params?.value as number })
          : '',
    },
    {
      field: 'discountPossible',
      headerName: 'Discount possible',
      width: 150,
      valueFormatter: (params) =>
        params.value
          ? formatNumberWithCommas({ value: params?.value as number })
          : '',
    },
  ]);

  const customTheme = themeQuartz.withParams({
    borderColor: 'var(--border-light)',
    wrapperBorder: false,
    headerRowBorder: false,
    rowBorder: { style: 'solid', width: 1, color: 'var(--border-light)' },
    columnBorder: { style: 'none' },
    backgroundColor: 'var(--background-card)',
    textColor: 'var(--text-light)',
  });

  const defaultColDef: ColDef = {
    flex: 1,
    resizable: true,
    sortable: true,
    filter: true,
  };

  if (!showGrid) return <PaymentTablleSkeleton />;

  return (
    <div
      className="ag-theme-alpine"
      style={{ height: '100%', width: '100%', border: 'none' }}
    >
      <AgGridReact
        enableCharts
        cellSelection={true}
        rowData={rowData}
        columnDefs={colDefs as any}
        defaultColDef={defaultColDef}
        animateRows={true}
        pinnedBottomRowData={[totalRow]}
        theme={customTheme}
        getRowStyle={(params) => {
          if (params.node.data && params.node.data.company === 'Total') {
            return { fontWeight: 'bold' };
          }
          return {};
        }}
      />
    </div>
  );
};

export default PaymentTermsTable;
