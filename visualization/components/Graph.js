import ApexCharts from 'apexcharts'

class Graph {
    constructor(id, state) {
        this.id = id
        this.state = state

        console.log(state)

        this.graph = new ApexCharts(
            document.querySelector("#" + id),
            this.state
        );

        this.graph.render()

        this.oldState = {
            keys: [],
            values: []
        }

        self = this
        this.anonCheck = function () {self.checkChange()}

        //setInterval(this.anonCheck, 100)
    }

    checkChange() {
        var stateKeys = Object.keys(this.state);
        var stateValues = Object.values(this.state);
        console.log(JSON.stringify(this.oldState.values) == JSON.stringify(stateValues))

        if (!( JSON.stringify(this.oldState.keys) == JSON.stringify(stateKeys) && JSON.stringify(this.oldState.values) == JSON.stringify(stateValues))){
            this.graph.updateOptions(this.state)
            console.log("this")
        }

        this.oldState.keys = Object.keys(this.state)
        this.oldState.values = Object.values(this.state)
    }

    update() {
        this.graph.updateOptions(this.state)
    }



}

export { Graph }