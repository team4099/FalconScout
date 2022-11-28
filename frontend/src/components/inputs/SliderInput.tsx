import React from "react"
import { ComponentSetup } from "../interface"

function SliderInput(props: ComponentSetup) {

    const updateStateText = (event) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = event.target.value
		props.setValue(state)
	}

    return (
		<div className="mx-3 my-3">
            <label className="block mb-2 text-sm text-gray-[#344054]">{props.text}</label>
            <input type="range" id="volume" name="volume" min={props.options?.[0]} max={props.options?.[1]} className="w-full bg-red" onChange={updateStateText}/>
            <div className="container h-6">
                <label className="block mb-2 text-sm text-gray-[#344054] float-left inline">
                    {props.options?.[0]}
                </label>
                <label className="block mb-2 text-sm text-gray-[#344054] float-right text-right inline">
                    {props.options?.[1]}
                </label>
            </div>
		</div>

  	)
}

export default SliderInput
