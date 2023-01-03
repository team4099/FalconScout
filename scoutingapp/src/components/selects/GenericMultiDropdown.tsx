import React from "react"
import { ComponentSetup } from "../interface"

function GenericMultiDropdown(props: ComponentSetup) {

	//is this even working tbh


    return (
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
			</label>
			<select name="option" id="options" className="appearance-none border border-color-[#D0D5DD] rounded w-full py-2 px-3 text-gray-700 focus:outline-none">
                { props.options?.map (option => (
                    <option value={option}>
						<input type="checkbox" id={option} name={option} value={option}/>
						{option}
					</option>
                ))}
            </select>
		</div>
  	)
}

export default GenericMultiDropdown