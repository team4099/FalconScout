import ApexCharts from 'apexcharts'
import { BarGraph } from './components/BarGraph';
import { LineGraph } from './components/LineGraph';
import { ScatterGraph } from './components/ScatterGraph';
import { PieGraph } from './components/PieGraph';
import { CalculatedStats } from './data/CalculatedStats';
import { Selections, Queries } from './data/Constants';

//var data = await fetch('data/iri_data.json').then(response => response.json())

(async () => {
  var data = await fetch('https://raw.githubusercontent.com/team4099/FalconScout/visualizations/visualization/data/iri_data.json').then(res => res.json())

  var stats = new CalculatedStats(data)

  var driverRating = new BarGraph(
    "plt1",
    "Avr Driver Rating by Team",
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
    "plt2",
    "Shooter over matches",
    {},
    {
      formula: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      selectedOption: 2056,
      allOptions: Selections.TEAMS
    }
  )

  var goodShooters = new ScatterGraph(
    "plt3",
    "Shooting by match by team",
    {},
    {
      formulaX: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      formulaY: function(team) {return stats.getScoreData(team, Queries.AUTO_UPPER_HUB)},
      selectedOptions: [4099, 2056],
      allOptions: Selections.TEAMS
    }
  )

  var gameContribution = new PieGraph(
    "plt4",
    "shooting contrib by match",
    {},
    {
      formula: function(match) {return stats.getMatchAllianceData(match, Queries.TELEOP_UPPER_HUB, Selections.RED)},
      selectedOption: "qm1",
      allOptions: Selections.MATCHES
    }
  )

  var driverRating = new BarGraph(
    "plt5",
    "Avr Driver Rating by Team",
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
    "plt6",
    "Shooter over matches",
    {},
    {
      formula: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      selectedOption: 2056,
      allOptions: Selections.TEAMS
    }
  )

  var goodShooters = new ScatterGraph(
    "plt7",
    "Shooting by match by team",
    {},
    {
      formulaX: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      formulaY: function(team) {return stats.getScoreData(team, Queries.AUTO_UPPER_HUB)},
      selectedOptions: [4099, 2056],
      allOptions: Selections.TEAMS
    }
  )

  var LContribution = new PieGraph(
    "plt8",
    "shooting contrib by match",
    {},
    {
      formula: function(match) {return stats.getMatchAllianceData(match, Queries.TELEOP_UPPER_HUB, Selections.RED)},
      selectedOption: "qm1",
      allOptions: Selections.MATCHES
    }
  )

  var plt9 = new BarGraph(
    "plt9",
    "Avr Driver Rating by Team",
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

  var plt10 = new LineGraph(
    "plt10",
    "Shooter over matches",
    {},
    {
      formula: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      selectedOption: 2056,
      allOptions: Selections.TEAMS
    }
  )

  var plt11 = new ScatterGraph(
    "plt11",
    "Shooting by match by team",
    {},
    {
      formulaX: function(team) {return stats.getScoreData(team, Queries.TELEOP_UPPER_HUB)},
      formulaY: function(team) {return stats.getScoreData(team, Queries.AUTO_UPPER_HUB)},
      selectedOptions: [4099, 2056],
      allOptions: Selections.TEAMS
    }
  )

  var plt12 = new PieGraph(
    "plt12",
    "shooting contrib by match",
    {},
    {
      formula: function(match) {return stats.getMatchAllianceData(match, Queries.TELEOP_UPPER_HUB, Selections.RED)},
      selectedOption: "qm1",
      allOptions: Selections.MATCHES
    }
  )
  })();