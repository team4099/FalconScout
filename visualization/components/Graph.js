import ApexCharts from 'apexcharts'

class Graph {
    constructor(id, chartOptions, plotOptions, seriesOptions) {
        this.id = id
        this.options = {
            chart: chartOptions,
            plotOptions: plotOptions,
            series: seriesOptions
        }
        this.graph =  new ApexCharts(
            document.querySelector("#" + id),
            this.options
        );

        this.graph.render();
    }

    set chart(chartOptions){
        this.options.chart = chartOptions
        this.graph.updateOptions(this.options)
    }

    set plotOptions(plotOptions){
        this.options.plotOptions = plotOptions
        this.graph.updateOptions(this.options)
    }

    set series(seriesOptions){
        this.options.series = seriesOptions
        this.graph.updateOptions(this.options)
    }



}

export { Graph }