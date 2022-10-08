import { Graph } from "./Graph"

class BarGraph {
    constructor(id, plotOptions, dataOptions){
        this.uuid = Math.random().toString(36).substr(2, 9)

        this.container = document.getElementById(id)
        this.container.setAttribute("type", "button")
        this.container.setAttribute("data-modal-toggle", this.uuid)

        var self = this
        this.container.addEventListener("click", function(){
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
                type: 'bar'
            },
            plotOptions,
            [{
                data: this.seriesOptions
            }]
        )

    }

    generateData(){
        this.seriesOptions = []

        for (const selected of this.selectedColumnOptions){
            this.seriesOptions.push(
                {
                    x: selected.toString(),
                    y: this.formula(selected)
                }
            )
        }
    }

    setupEdit(){
        var formString = ``

        var self = this
        document.getElementById("getEditedData").addEventListener("click", function(){
            self.pushEdit()
        })

        for (const i of this.allColumnOptions){
            if (this.selectedColumnOptions.includes(i)){
                formString += `
                <div class="flex items-center">
                    <input checked id="${i}" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label for="${i}" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">${i}</label>
                </div>
                `
            }
            else {
                formString += `
                <div class="flex items-center">
                    <input id="${i}" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"/>
                    <label for="${i}" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">${i}</label>
                </div>
                `
            }
        }

        document.getElementById("editableFormContainer").innerHTML = formString
        
    }

    pushEdit() {
        this.selectedColumnOptions = []
        for (const i of this.allColumnOptions){
            if (document.getElementById(i.toString()).checked){
                this.selectedColumnOptions.push(i)
            }
        }

        this.generateData()

        this.graph.series = [{
            data: this.seriesOptions
        }]
    }
}


export { BarGraph }