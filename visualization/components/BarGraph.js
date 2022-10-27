import { Graph } from "./Graph"

class BarGraph {
    constructor(id, title, plotOptions, dataOptions, modal) {
        this.uuid = Math.random().toString(36).substr(2, 9)

        this.modal = modal

        this.container = document.getElementById(id)
        this.container.setAttribute("type", "button")
        this.container.setAttribute("data-modal-toggle", this.uuid)

        var self = this
        this.container.addEventListener("click", function () {
            self.setupEdit()
            document.getElementById('fakeToggle').click()
        })


        this.formula = dataOptions.formula

        this.selectedColumnOptions = dataOptions.selectedOptions
        this.allColumnOptions = dataOptions.allOptions

        this.generateData()

        this.graph = new Graph(
            id,
            {
                chart: {
                    type: 'bar',
                    zoom: {
                        enabled: true
                    },
                    animations: {
                        enabled: false
                    }
                },
                plotOptions: plotOptions,
                series: [{
                    data: this.seriesOptions
                }],
                title: {
                    text: title,
                    align: 'left'
                }
            }
        )

    }

    generateData() {
        this.seriesOptions = []

        for (const selected of this.selectedColumnOptions) {
            this.seriesOptions.push(
                {
                    x: selected.toString(),
                    y: this.formula(selected)
                }
            )
        }
    }

    setupEdit() {
        var formString = ``

        var self = this
        this.modal.setCallBackClose(function () {
            self.pushEdit()
        })

        for (const i of this.allColumnOptions) {
            if (this.selectedColumnOptions.includes(i)) {
                formString += `
                <div class="flex items-center">
                    <input checked id="${i}${this.uuid}" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label id="for="${i}${this.uuid}" class="ml-2 text-sm font-medium text-gray-300">${i}</label>
                </div>
                `
            }
            else {
                formString += `
                <div class="flex items-center">
                    <input id="${i}${this.uuid}" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label for="${i}${this.uuid}" class="ml-2 text-sm font-medium text-gray-300">${i}</label>
                </div>
                `
            }
        }

        this.modal.formHTML = formString

    }

    pushEdit() {
        this.selectedColumnOptions = []
        for (const i of this.allColumnOptions) {
            if (document.getElementById(i.toString() + this.uuid.toString()).checked) {
                this.selectedColumnOptions.push(i)
            }
        }

        this.generateData()

        this.graph.state.series = [{
            data: this.seriesOptions
        }]

        this.graph.update()

    }
}


export { BarGraph }
