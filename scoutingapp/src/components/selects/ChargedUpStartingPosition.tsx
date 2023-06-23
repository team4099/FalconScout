import { useState } from "react"
import { ComponentSetup } from "../interface"
import "./index.css"

function ChargedUpStartingPosition(props: ComponentSetup) {

	const [toggleValue, setToggleValue] = useState("")

	function toggle(switchValue: any) {
		if (toggleValue == switchValue) {
			setToggleValue("")
			updateStateSelections("")
		} else {
			setToggleValue(switchValue)
			updateStateSelections(switchValue)
		}
	}

	const updateStateSelections = (newValue: any) => {
		var state = props.getValue
		state[props.id] = newValue
		props.setValue(state)
	}

    return (
		<div className="mx-3 my-3 flex flex-col items-center">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
			</label>
			<div className=" flex gap-16 flex-col pl-24 pt-7 bg-[url('../public/fieldMapBlue.png')] w-[19.5rem] h-[22.5rem] bg-contain bg-no-repeat">
				<div className={`rounded-lg h-16 w-20 text-center font-bold pt-2 ${toggleValue == "Loading Zone" ? "bg-blue-500" : "bg-blue-200"}`} onClick={()=>toggle("Loading Zone")}>
					Loading Zone
				</div>
				<div className={`rounded-lg h-16 w-20 text-center font-bold pt-2 ${toggleValue == "Charge Station" ? "bg-blue-500" : "bg-blue-200"}`} onClick={()=>toggle("Charge Station")}>
					Charge Station
				</div>
				<div className={`text-md rounded-lg h-16 w-20 text-center font-bold pt-2 ${toggleValue == "Cable Cover" ? "bg-blue-500" : "bg-blue-200"}`} onClick={()=>toggle("Cable Cover")}>
					Cable Cover
				</div>
			</div>
			<div className="my-3">
			<button className={`text-sm font-bold w-[20rem] py-2 px-2 rounded-lg ${toggleValue == "Not on Field" ? "bg-rose-500": "bg-rose-300"}`} onClick= {() => toggle("Not on Field")}>
                Not on Field
            </button>
		</div>
		</div>
  	)
}

export default ChargedUpStartingPosition