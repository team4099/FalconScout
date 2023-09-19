import React, { useState } from "react"
import { ComponentSetup } from "../interface"

function SliderInput(props: ComponentSetup) {

    const [value, setValue] = useState(props.placeholder?.[0])
    
    const updateStateText = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = event.target.value 
		props.setValue(state)
        setValue(event.target.value)
	}


    return (
		<div className="mx-3 my-3">
            <label className="block mb-2 text-sm text-gray-[#344054]">{props.text}</label>
            <input type="range" id="volume" name="volume" defaultValue={props.placeholder?.[0]} min={props.options?.[0]} step={props.options?.[2]} max={props.options?.[1]} className="w-full bg-red" onChange={updateStateText} onLoad={updateStateText}/>
            <div className="relative w-full container h-6">
                <label className="absolute block -ml-1 mb-2 text-sm text-gray-[#344054] left-0 p-1 inline">
                    {props.options?.[0]}
                </label>
                <label className="absolute block text-sm text-gray-[#344054] left-1/2 inline p-1 border-2 rounded-lg px-2 ">
                    {value}
                </label>
                <label className="absolute block -mr-1 mb-2 text-sm text-gray-[#344054] right-0 p-1 text-right inline">
                    {props.options?.[1]}
                </label>
            </div>
		</div>

  	)
}

export default SliderInput
