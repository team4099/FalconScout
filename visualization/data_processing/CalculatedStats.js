class CalculatedStats {
    constructor(data){
        this.data = data
    }

    getAvrDriverRating(team){
        try {
            var values = 0
            var total = 0
        
            for (const x of this.data[team]) { 
                total += x["Driver Rating"]; 
                values += 1
            }
    
            return (total/values).toFixed(2)
        }
        catch (e) {
            console.log(e)
            return 0
        }
    }
}

export { CalculatedStats }