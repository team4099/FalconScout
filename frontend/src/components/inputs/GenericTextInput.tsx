import React from "react"
import { ComponentSetup } from "../interface"

function GenericTextInput(props: ComponentSetup) {

	const updateStateText = (event) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = event.target.value
		props.setValue(state)
	}

    return (
    
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
			</label>
			<input 
				className="appearance-none border border-color-[#D0D5DD] rounded w-full py-2 px-3 text-gray-700 focus:outline-none" id="textInput" type="text" placeholder={props.placeholder?.[0]}
				onChange={updateStateText}
			></input>
		</div>

  	)
}

export default GenericTextInput
