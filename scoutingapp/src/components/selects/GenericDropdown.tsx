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
			<label className="block text-sm mb-2">
				{props.text}
				{ props.required == true && (
					<span className="ml-1  text-[var(--default-deep-red)] font-bold">
						*	
					</span>
				)}
			</label>
			<select name="option" defaultValue="" onChange={updateStateSelections} id="options" className="appearance-none border border-color-[#D0D5DD] rounded w-full py-2 px-3 focus:outline-none">
				<option disabled value=""> -- </option>
				{ props.options?.map ((option: string, key: number) => (
                    <option key={key} value={option}>{option}</option>
                ))}
            </select>
		</div>

  	)
}

export default GenericDropdown
