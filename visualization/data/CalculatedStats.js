class CalculatedStats {
    constructor(data){
        this.data = data
    }

    getAvrDriverRating(team){
        try {
            var values = 0
            var total = 0
        
            for (const x of this.data[team]) { 
                total += x["Defense Rating"]; 
                values += 1
            }
    
            return (total/values).toFixed(2)
        }
        catch (e) {
            return 0
        }
    }

    getScoreData(team, stat){
        try {
            var match = []
            var scored = []
        
            for (const x of this.data[team]) { 
                match.push(x["Match Key"])
                scored.push(x[stat])
            }
    
            return [match, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }

    getMatchAllianceData(match, stat, alliance){
        try {
            var teams = []
            var scored = []
        
            for (const x of Object.values(this.data)) { 
                for (const l of x){
                    if (l["Match Key"] == match && l["Alliance"] == alliance){
                        teams.push(l["Team Number"].toString())
                        scored.push(l[stat])
                        break
                    }
                }
            }
    
            return [teams, scored]
        }
        catch (e) {
            return [[0], [0]]
        }
    }
}

export { CalculatedStats }