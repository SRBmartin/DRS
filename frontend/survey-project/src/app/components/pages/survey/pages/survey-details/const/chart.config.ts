import { ChartOptions, ChartData, ChartType } from 'chart.js';

export const DEFAULT_CHART_TYPE: ChartType = 'bar';
export const DEFAULT_CHART_LEGEND = false;

export const DEFAULT_CHART_OPTIONS: ChartOptions = {
  responsive: true,
  indexAxis: 'y',
  scales: {
    x: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: (value: number | string) => `${value}%`
      }
    }
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => `${context.parsed.x}%`
      }
    }
  }
};

export const INITIAL_CHART_DATA: ChartData<'bar', number[], string | string[]> = {
  labels: ['Yes', 'No', 'Maybe'],
  datasets: [{
    data: [0, 0, 0],
    backgroundColor: ['#4CAF50', '#F44336', '#9E9E9E']
  }]
};
