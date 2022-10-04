import ApexCharts from 'apexcharts'

const data = await fetch('iri_data.json').then(response => response.json())

function getAvrDriverRating(team){
	var values = 0
	var total = 0

	for (const x of data[team]) { 
		total += x["Driver Rating"]; 
		values += 1
	}
	
	return (total/values).toFixed(2)
}

var options = {
  chart: {
    type: 'bar'
  },
  plotOptions: {
    bar: {
      horizontal: false
    }
  },
  series: [{
    data: [{
      x: '2363',
      y: getAvrDriverRating(2363)
    }, {
      x: '5406',
      y: getAvrDriverRating(5406)
    }, {
      x: '4099',
      y: getAvrDriverRating(4099)
    }]
  }]
}

function test(){
  var chart = new ApexCharts(
    document.querySelector("#visBox"),
    options
  );

  chart.render();

  chart.updateOptions(options)
}

test()
