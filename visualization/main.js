import ApexCharts from 'apexcharts'
import { BarGraph } from './components/BarGraph';
import { LineGraph } from './components/LineGraph';
import { ScatterGraph } from './components/ScatterGraph';
import { PieGraph } from './components/PieGraph';
import { CalculatedStats } from './data/CalculatedStats';
import { Selections, Queries } from './data/Constants';

var data = await fetch('data/iri_data.json').then(response => response.json())
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
    allOptions: Selections.TEAMS
  }
)

var shooterOverTime = new LineGraph(
  "lineBox",
  {},
  {
    formula: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
    selectedOption: 2056,
    allOptions: Selections.TEAMS
  }
)

var goodShooters = new ScatterGraph(
  "scatterBox",
  {},
  {
    formulaX: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
    formulaY: function(team) {return stats.getScoreData(team, Queries.AUTO_UPPER_HUB)},
    selectedOptions: [4099, 2056],
    allOptions: Selections.TEAMS
  }
)

var gameContribution = new PieGraph(
  "pieBox",
  {},
  {
    formula: function(match) {return stats.getMatchAllianceData(match, Queries.TELEOP_UPPER_HUB, Selections.RED)},
    selectedOption: "qm1",
    allOptions: Selections.MATCHES
  }
)