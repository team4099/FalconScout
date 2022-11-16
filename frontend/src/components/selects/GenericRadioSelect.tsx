import { ComponentSetup } from "../interface"
import "./index.css"

function GenericRadioSelect(props: ComponentSetup) {

    return (
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
			</label>
			<form>
                <div className="flex flex-wrap">
                    <div className="w-1/2 px-1">
                        { props.options?.slice(0, Math.ceil(props.options?.length / 2)).map (option => (
                            <div className="mb-1">
                                <input type="radio" id={option} name="Selection" value={option} className="radio"/>
                                <p className="ml-3 inline">{option}</p>
                            </div>
                        ))}
                    </div>
                    <div className="w-1/2 px-1">
                        { props.options?.slice(Math.ceil(props.options?.length / 2)).map (option => (
                            <div className="mb-1">
                                <input type="radio" id={option} name="Selection" value={option} className="radio"/>
                                <p className="inline ml-3">{option}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </form>
		</div>
  	)
}

export default GenericRadioSelect