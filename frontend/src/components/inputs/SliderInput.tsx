import { ComponentSetup } from "../interface"

function SliderInput(props: ComponentSetup) {
    return (
		<div className="mx-3 my-3">
            <label className="block mb-2 text-sm text-gray-[#344054]">{props.text}</label>
            <input type="range" id="volume" name="volume" min="0" max="11" className="w-full bg-red"/>
            <div>
                <label className="block mb-2 text-sm text-gray-[#344054] float-left inline">
                    {props.options?.[0]}
                </label>
                <label className="block mb-2 text-sm text-gray-[#344054] float-right inline">
                    {props.options?.[1]}
                </label>
            </div>
		</div>

  	)
}

export default SliderInput
