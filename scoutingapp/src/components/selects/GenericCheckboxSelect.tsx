import React from "react"
import { ComponentSetup } from "../interface"
import "./index.css"

function GenericCheckboxSelect(props: ComponentSetup) {

    const updateStateSelections = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue

        var values = Array()
        const checks = document.getElementsByClassName("radio " + props.id) as HTMLCollectionOf<HTMLInputElement>;
        for (const check of checks) {
            if (check.checked) {
              values.push(check.value)
            }
          }

		state[props.id] = values
		props.setValue(state)
	}

    return (
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
			</label>
			<form onChange={updateStateSelections}>
                <div className="flex flex-wrap">
                    <div className="w-1/2 px-1">
                        { props.options?.slice(0, Math.ceil(props.options?.length / 2)).map (option => (
                            <div className="mb-1">
                                <input type="checkbox" name={option} value={option} className={`radio ${props.id}`}/>
                                <p className="ml-3 inline">{option}</p>
                            </div>
                        ))}
                    </div>
                    <div className="w-1/2 px-1">
                        { props.options?.slice(Math.ceil(props.options?.length / 2)).map (option => (
                            <div className="mb-1">
                                <input type="checkbox" name={option} value={option} className={`radio ${props.id}`}/>
                                <p className="inline ml-3">{option}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </form>
		</div>
  	)
}

export default GenericCheckboxSelect