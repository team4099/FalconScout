import React from "react"
import { ComponentSetup } from "../interface"
import { useTheme } from "../ThemeContext"
import "./index.css"

function GenericToggle(props: ComponentSetup) {
	const { theme } = useTheme();

	const updateState = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = event.target.checked
		props.setValue(state)
	}

    return (
		<div className="mx-3 my-3">
			<label className="block text-sm mb-2" style={{color: theme === 'light' ? '#000000' : '#FFFFFF'}}>
				{props.text}
			</label>
			
            <label className="switch">
                <input type="checkbox" onChange={updateState}/>
                <span className="slider round"></span>
            </label>
            
		</div>
  	)
}

export default GenericToggle