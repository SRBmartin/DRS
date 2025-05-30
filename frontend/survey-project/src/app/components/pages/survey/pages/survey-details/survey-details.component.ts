import { Component } from '@angular/core';
import { ChartData, ChartType } from 'chart.js';

@Component({
  selector: 'app-survey-details',
  templateUrl: './survey-details.component.html',
  styleUrl: './survey-details.component.scss'
})
export class SurveyDetailsComponent {
  public pieChartType: ChartType = 'pie';
  public pieChartLegend = true;
  public pieChartOptions = {
    responsive: true
  };

  public pieChartData: ChartData<'pie', number[], string | string[]> = {
    labels: ['Opcija 1', 'Opcija 2', 'Opcija 3'],
    datasets: [
      {
        data: [45, 25, 30]
      }
    ]
  };
}
