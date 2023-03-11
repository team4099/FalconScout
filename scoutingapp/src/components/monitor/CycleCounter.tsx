import React, { useState } from "react"
import { ComponentSetup } from "../interface"

export function CycleCounter(props: ComponentSetup) {

	const updateStateDropdown = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id][0] = event.target.value
		props.setValue(state)
	}

    const updateStateText = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id][1] = event.target.value
		props.setValue(state)
	}

    var stampFPGA = new Date().getTime()
    var monitorValues: any = {}
    if (props?.options != undefined){
        for (var i=0; i < props?.options?.length && props?.options; i++){
            monitorValues[props?.options[i]] = props.getValue[props?.options[i]]
            console.log(props.getValue[props?.options[i]])
        }
    }
    const [totalTime, setTotalTime] = useState(0)
    const [cycles, setCycles] = useState(0)

    setInterval(() => {
        if (props?.options != undefined){
            for (var i=0; i < props?.options?.length && props?.options; i++){
                var currentValue = props.getValue[props?.options[i]]
                // console.log(totalTime)
                // console.log(cycles)
                if (currentValue != monitorValues[props?.options[i]]){
                    console.log("running")
                    setTotalTime(new Date().getTime() - stampFPGA + totalTime)
                    setCycles(cycles + 1)
                    stampFPGA = new Date().getTime()
                }
                monitorValues[props?.options[i]] = props.getValue[props?.options[i]]
            }
        }
    }, 50)

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                { props.text }
            </label>

            <label className="block text-[#344054] text-sm mb-2">
                Avr time: { (totalTime) } { cycles }
            </label>
        </div>
    )

}