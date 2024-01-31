import React from "react"
import { ComponentSetup } from "../interface"

function DropdownTextInput(props: ComponentSetup) {

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

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                { props.text }
                { props.required == true && (
					<span className="ml-1 text-red-400 font-bold">
						*	
					</span>
				)}
            </label>
            <div className="flex appearance-none h-[40px] border border-color-[#D0D5DD] border-[1.5px] rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                <select name="option" id="options" className="inline" onChange={updateStateDropdown}>
                    <option disabled selected value=""> -- </option>
                    { props.options?.map (option => (
                        <option value={option}>{option}</option>
                    ))}
                </select>

                <input className="text-black pl-4 focus:outline-none inline flex-grow w-full" placeholder={props.placeholder?.[0]} onChange={updateStateText} >
                </input>
            </div>
        </div>
    )
}
  
export default DropdownTextInput
  