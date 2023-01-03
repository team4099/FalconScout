import React from "react"
import {ComponentSetup} from "../interface"

function DarkButton(props: ComponentSetup) {

	const updateState = () => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = true
		props.setValue(state)
	}

    return (
    
		<div className="mx-3 my-3">
			<button className="bg-black text-sm font-semibold outline w-full hover:outline-3 hover:outline-gray-300 text-white py-2 px-2 rounded-lg" onClick={updateState}>
                { props.text }
            </button>
		</div>

  	)
}

export default DarkButton
