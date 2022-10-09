import ApexCharts from 'apexcharts'
import { BarGraph } from './components/BarGraph';
import { CalculatedStats } from './data_processing/CalculatedStats';

var data = await fetch('iri_data.json').then(response => response.json())
var stats = new CalculatedStats(data)

var driverRating = new BarGraph(
  "visBox",
  {
    bar: {
      horizontal: false
    }
  },
  {
    formula: function(team) {return stats.getAvrDriverRating(team)},
    selectedOptions: [4099, 118, 180],
    allOptions: [33, 2056, 4499, 2468, 4099, 118, 180]
  }
)
