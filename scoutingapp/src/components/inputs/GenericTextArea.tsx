import React from "react"
import { ComponentSetup } from "../interface"
import { useTheme } from "../ThemeContext"

function GenericTextArea(props: ComponentSetup){
    const { theme } = useTheme();

    const updateStateText = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = event.target.value
		props.setValue(state)
	}

    const textColor = theme === 'light' ? '#000000' : '#FFFFFF';

    return (
    
		<div className="mx-3 my-3">
			<label className="block mb-2 text-sm text-gray-[#344054]">{props.text}</label>
			<textarea id="message" className="block py-2 px-3 w-full h-40 text rounded-lg border border-color-[#D0D5DD] focus:outline-none" style={{color: textColor}} placeholder={props.placeholder?.[0]} onChange={updateStateText}></textarea>
		</div>

  	)
}

export default GenericTextArea
