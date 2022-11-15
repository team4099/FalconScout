import { ComponentSetup } from "../interface"
import "./index.css"

function GenericToggle(props: ComponentSetup) {

    return (
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
			</label>
			
            <label className="switch">
                <input type="checkbox"/>
                <span className="slider round"></span>
            </label>
            
		</div>
  	)
}

export default GenericToggle