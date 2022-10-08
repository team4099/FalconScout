import ApexCharts from 'apexcharts'
import { BarGraph } from './components/BarGraph';

const data = await fetch('iri_data.json').then(response => response.json())

function getAvrDriverRating(team){
  try {
    var values = 0
    var total = 0

    for (const x of data[team]) { 
      total += x["Driver Rating"]; 
      values += 1
    }
	
	  return (total/values).toFixed(2)
  }
  catch {
    return 0
  }
}

var driverRating = new BarGraph(
  "visBox",
  {
    bar: {
      horizontal: false
    }
  },
  {
    formula: getAvrDriverRating,
    selectedOptions: [4099, 118, 180],
    allOptions: [33, 2056, 4499, 2468, 4099, 118, 180]
  }
)
