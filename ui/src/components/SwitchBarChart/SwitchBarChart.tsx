import { useState } from 'react';
import { AgCharts } from 'ag-charts-react';
import { AgChartOptions } from 'ag-charts-community';
import 'ag-charts-enterprise';

const supplierData = [
  { supplier: 'Supplier 1', sales: 180 },
  { supplier: 'Supplier 2', sales: 154 },
  { supplier: 'Supplier 3', sales: 140 },
  { supplier: 'Supplier 4', sales: 120 },
  { supplier: 'Supplier 5', sales: 110 },
  { supplier: 'Supplier 6', sales: 90 },
  { supplier: 'Supplier 7', sales: 75 },
  { supplier: 'Supplier 8', sales: 60 },
];

const plantData = [
  { plant: 'Plant 1', sales: 210 },
  { plant: 'Plant 2', sales: 190 },
  { plant: 'Plant 3', sales: 170 },
  { plant: 'Plant 4', sales: 160 },
  { plant: 'Plant 5', sales: 150 },
  { plant: 'Plant 6', sales: 130 },
  { plant: 'Plant 7', sales: 110 },
  { plant: 'Plant 8', sales: 95 },
  { plant: 'Plant 9', sales: 75 },
  { plant: 'Plant 10', sales: 55 },
];

const countryData = [
  { country: 'Germany', sales: 220 },
  { country: 'France', sales: 195 },
  { country: 'USA', sales: 175 },
  { country: 'China', sales: 155 },
  { country: 'UK', sales: 135 },
  { country: 'Italy', sales: 120 },
  { country: 'Netherlands', sales: 105 },
  { country: 'Spain', sales: 85 },
  { country: 'Canada', sales: 65 },
  { country: 'Japan', sales: 45 },
];

const skuData = [
  { sku: 'SKU1', sales: 200 },
  { sku: 'SKU2', sales: 185 },
  { sku: 'SKU3', sales: 165 },
  { sku: 'SKU4', sales: 145 },
  { sku: 'SKU5', sales: 125 },
  { sku: 'SKU6', sales: 115 },
  { sku: 'SKU7', sales: 95 },
  { sku: 'SKU8', sales: 80 },
  { sku: 'SKU9', sales: 70 },
  { sku: 'SKU10', sales: 50 },
];

const SwitchableBarChart = () => {
  const [activeView, setActiveView] = useState<
    'Plant' | 'Supplier' | 'Country' | 'SKU'
  >('Supplier');

  const dataMap = {
    Plant: { data: plantData, xKey: 'plant' },
    Supplier: {
      data: supplierData,
      xKey: 'supplier',
    },
    Country: { data: countryData, xKey: 'country' },
    SKU: { data: skuData, xKey: 'sku' },
  };

  const { data, xKey } = dataMap[activeView];

  const chartOptions: AgChartOptions = {
    background: {
      fill: 'transparent',
    },
    data,
    series: [
      {
        type: 'bar',
        xKey,
        yKey: 'sales',
        yName: 'Sales',
        fill: 'rgba(34, 81, 255, 1)',
        label: {
          enabled: true,
          color: 'white',
          fontSize: 12,
          placement: 'inside-center',
          formatter: ({ value }) => `${value}M`,
        },
      },
    ],
    axes: [
      {
        type: 'category',
        position: 'bottom',
        gridLine: { enabled: false },
        label: { color: 'rgba(255, 255, 255, 0.8)' },
      },
      {
        type: 'number',
        position: 'left',
        gridLine: { enabled: false },
        label: {
          formatter: ({ value }) => `${value}M`,
          color: 'rgba(255, 255, 255, 0.8)',
        },
      },
    ],
  };

  return (
    <div className="switchable-chart-container">
      <div className="switchable-chart-buttons">
        <div className="switchable-chart-button-group">
          {(['Plant', 'Supplier', 'Country', 'SKU'] as const).map((view) => (
            <button
              key={view}
              className={`switchable-chart-button ${activeView === view ? 'active' : ''}`}
              onClick={() => setActiveView(view)}
            >
              {view}
            </button>
          ))}
        </div>
      </div>
      <div className="switchable-chart">
        <AgCharts options={chartOptions as AgChartOptions} />
      </div>
    </div>
  );
};

export default SwitchableBarChart;
