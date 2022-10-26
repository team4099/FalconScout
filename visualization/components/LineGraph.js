import { Graph } from "./Graph"

class LineGraph {
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

        this.selectedOption = dataOptions.selectedOption
        this.allOptions = dataOptions.allOptions

        this.generateData()

        this.graph = new Graph(
            id,
            {
                chart: {
                    type: 'line',
                    zoom: {
                        enabled: false
                    }
                },
                plotOptions: plotOptions,
                series: [{
                    name: this.selectedOption.toString(),
                    data: this.yAxis
                }],
                xaxis: {
                    categories: this.xAxis,
                },
                title: {
                    text: title,
                    align: 'left'
                }
            }
        )

    }

    generateData() {
        [this.xAxis, this.yAxis] = this.formula(this.selectedOption)
    }

    setupEdit() {
        var formString = `<fieldset class="space-y-6">`

        var self = this
        this.modal.setCallBackClose(function () {
            self.pushEdit()
        })

        for (const i of this.allOptions) {
            if (this.selectedOption == i) {
                formString += `
                <div class="flex items-center">
                    <input checked id="${i}${this.uuid}" type="radio" value="" name="team" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label id="for="${i}${this.uuid}" class="ml-2 text-sm font-medium text-gray-300">${i}</label>
                </div>
                `
            }
            else {
                formString += `
                <div class="flex items-center">
                    <input id="${i}${this.uuid}" type="radio" value="" name="team" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label for="${i}${this.uuid}" class="ml-2 text-sm font-medium text-gray-300">${i}</label>
                </div>
                `
            }
        }

        formString += `</fieldset>`

        this.modal.formHTML = formString
    }

    pushEdit() {
        this.selectedOption = 0
        for (const i of this.allOptions) {
            if (document.getElementById(i.toString() + this.uuid.toString()).checked) {
                this.selectedOption = i
            }
        }

        this.generateData()

        this.graph.state.series = [{
                name: this.selectedOption.toString(),
                data: this.yAxis
            }
        ]

        this.graph.update()
    }
}


export { LineGraph }