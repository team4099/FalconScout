import React from "react"
import { ComponentSetup } from "../interface"

function GenericTextArea(props: ComponentSetup){

    const updateStateText = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = event.target.value
		props.setValue(state)
	}

    return (
    
		<div className="mx-3 my-3">
			<label className="block mb-2 text-sm text-gray-[#344054]">{props.text}</label>
			<textarea id="message" className="block py-2 px-3 w-full h-40 text text-[#000000] rounded-lg border border-color-[#D0D5DD] focus:outline-none" placeholder={props.placeholder?.[0]} onChange={updateStateText}></textarea>
		</div>

  	)
}

export default GenericTextArea
