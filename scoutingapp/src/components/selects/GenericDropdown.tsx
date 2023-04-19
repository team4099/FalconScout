import React from "react"
import { ComponentSetup } from "../interface"

function GenericDropdown(props: ComponentSetup) {

	const updateStateSelections = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue

        var e = document.getElementById("ddlViewBy");
		var value = event.target.value;
		var text = event.target.options[event.target.selectedIndex].text;

		state[props.id] = text
		props.setValue(state)
	}

    return (
    
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
				{ props.required == true && (
					<span className="ml-1 text-red-400 font-bold">
						*	
					</span>
				)}
			</label>
			<select name="option" onChange={updateStateSelections} id="options" className="appearance-none border border-color-[#D0D5DD] rounded w-full py-2 px-3 text-gray-700 focus:outline-none">
				<option disabled selected value=""> -- </option>
				{ props.options?.map (option => (
                    <option value={option}>{option}</option>
                ))}
            </select>
		</div>

  	)
}

export default GenericDropdown
