import { Graph } from "./Graph"

class PieGraph {
    constructor(id, title, plotOptions, dataOptions, modal, editable = true) {
        this.uuid = Math.random().toString(36).substr(2, 9)

        this.modal = modal

        this.container = document.getElementById(id)
        this.container.setAttribute("type", "button")
        this.container.setAttribute("data-modal-toggle", this.uuid)

        var self = this
        if (editable) {
            this.container.addEventListener("click", function () {
                self.setupEdit()
                document.getElementById('fakeToggle').click()
            })
        }


        this.formula = dataOptions.formula

        this.selectedOption = dataOptions.selectedOption
        this.allOptions = dataOptions.allOptions

        this.generateData()

        this.graph = new Graph(
            id,
            {
                chart: {
                    type: 'pie',
                    zoom: {
                        enabled: false
                    },
                    animations: {
                        enabled: false
                    }
                },
                plotOptions: plotOptions,
                series: this.series,
                labels: this.labels,
                title: {
                    text: title,
                    align: 'left'
                },
            }
        )

    }

    generateData() {
        [this.labels, this.series] = this.formula(this.selectedOption)
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

        this.graph.state.series = this.series
        this.graph.state.labels = this.labels

        this.graph.update()
    }
}


export { PieGraph }

var options = {
    series: [44, 55, 13, 43, 22],
    chart: {
        width: 380,
        type: 'pie',
    },
    labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
};