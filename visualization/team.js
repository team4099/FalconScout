import { CalculatedStats } from './data/CalculatedStats';
import { StatNumber } from './components/StatNumber';
import { Queries } from './data/Constants'

(async () => {
    var data = await fetch('data/iri_data.json').then(res => res.json())

    var stats = new CalculatedStats(data)

    var falconRank = new StatNumber(
        4099, 
        "falcon_rank", 
        function (team) { return stats.getFalconRank(team) }, 
        2
    )
    var uptime = new StatNumber(
        4099, 
        "uptime", 
        function (team) { return stats.getAvrStat(team, Queries.UPTIME) }, 
        0.5
    )
    var teleop_upper = new StatNumber(
        4099, 
        "avr_teleop_upper", 
        function (team) { return stats.getAvrStat(team, Queries.TELEOP_UPPER_HUB)}, 
        15
    )
    var auto_upper = new StatNumber(
        4099, 
        "avr_auto_upper", 
        function (team) { return stats.getAvrStat(team, Queries.AUTO_UPPER_HUB)}, 
        2
    )
    var driver_rating = new StatNumber(
        4099, 
        "driver_rating", 
        function (team) { return stats.getAvrStat(team, Queries.DRIVER_RATING) }, 
        2
    )
    var defense_rating = new StatNumber(
        4099, 
        "defense_rating", 
        function (team) { return stats.getAvrStat(team, Queries.DEFENSE_RATING) }, 
        2
    )

    var setTeams = function () {
        var team = document.getElementById("teams").value
        falconRank.team = team
        uptime.team = team
        teleop_upper.team = team
        auto_upper.team = team
        driver_rating.team = team
        defense_rating.team = team
    }

    setTeams()

    document.getElementById("teams").addEventListener("change", setTeams)

})()