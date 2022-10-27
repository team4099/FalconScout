class StatNumber {
    constructor(team, id, formula, threshold){
        this.formula = formula
        this.id = id
        this.threshold = threshold
        this.team = team
        
    }
    set team(newTeam){
        var result = 0
        result = this.formula(newTeam)
        
        document.getElementById(this.id).innerHTML = result.toString()
        if (result < this.threshold){
            document.getElementById(this.id).style.color = "#ff4a4a"
        }
        else if (result > this.threshold){
            document.getElementById(this.id).style.color = "#248e24"
        }
        else {
            document.getElementById(this.id).style.color = "#000000"
        }
    }
}

export { StatNumber }