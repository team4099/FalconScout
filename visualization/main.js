import ApexCharts from 'apexcharts'
import { BarGraph } from './components/BarGraph';
import { LineGraph } from './components/LineGraph';
import { ScatterGraph } from './components/ScatterGraph';
import { CalculatedStats } from './data_processing/CalculatedStats';

var data = await fetch('iri_data.json').then(response => response.json())
var stats = new CalculatedStats(data)

var driverRating = new BarGraph(
  "barBox",
  {
    bar: {
      horizontal: false
    }
  },
  {
    formula: function(team) {return stats.getAvrDriverRating(team)},
    selectedOptions: [4099, 118, 180],
    allOptions: [33, 2056, 4499, 2468, 4099, 118, 180, 340]
  }
)

var shooterOverTime = new LineGraph(
  "lineBox",
  {},
  {
    formula: function(team) {return stats.getScoreData(team, "Teleop Upper Hub")},
    selectedOption: 2056,
    allOptions: [33, 2056, 4499, 2468, 4099, 118, 180, 340]
  }
)

var goodShooters = new ScatterGraph(
  "scatterBox",
  {},
  {
    formulaX: function(team) {return stats.getScoreData(team, "Teleop Upper Hub")},
    formulaY: function(team) {return stats.getScoreData(team, "Auto Upper Hub")},
    selectedOptions: [4099, 2056],
    allOptions: [33, 2056, 4499, 2468, 4099, 118, 180, 340]
  }
)