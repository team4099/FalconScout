import React from "react"
import { ComponentSetup } from "../interface"
import "./index.css"

function GenericRadioSelect(props: ComponentSetup) {

    const updateStateSelections = (event: any) => {
		//console.log(props.getValue)
		var state = props.getValue

        var value = ""
        const checks = document.getElementsByClassName("radio " + props.id) as HTMLCollectionOf<HTMLInputElement>;
        for (const check of checks) {
            if (check.checked) {
              value = check.value
            }
          }

		state[props.id] = value
		props.setValue(state)
	}

    return (
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				{props.text}
                { props.required == true && (
					<span className="ml-1 text-red-400 font-bold">
						*	
					</span>
				)}
			</label>
			<form onChange={updateStateSelections}>
                {props.options?.length == 2 && props.options?.[0] == "red" && props.options?.[1] == "blue" &&
                    <div className="flex flex-row gap-2">
                        <div className="basis-1/2 p-1 pt-[8px] h-[3em] border-4 rounded-xl border-[#e5534b]">
                            <div className="mb-1 ml-2">
                                <input type="radio" id="red" name="Selection" value="red" className={`radio ${props.id}`}/>
                                <p className="ml-3 inline text-black font-semibold">red</p>
                            </div>
                        </div>
                        <div className="basis-1/2 p-1 pt-[8px] h-[3em] border-4 rounded-xl border-[#529bf5]">
                            <div className="mb-1 ml-2">
                                <input type="radio" id="blue" name="Selection" value="blue" className={`radio ${props.id}`}/>
                                <p className="ml-3 inline text-black font-semibold">blue</p>
                            </div>
                        </div>
                    </div>
                }
                {!(props.options?.length == 2 && props.options?.[0] == "red" && props.options?.[1] == "blue") &&
                    <div className="flex flex-wrap">
                        <div className="w-1/2 px-1">
                            { props.options?.slice(0, Math.ceil(props.options?.length / 2)).map (option => (
                                <div className="mb-1">
                                    <input type="radio" id={option} name="Selection" value={option} className={`radio ${props.id}`}/>
                                    <p className="ml-3 inline">{option}</p>
                                </div>
                            ))}
                        </div>
                        <div className="w-1/2 px-1">
                            { props.options?.slice(Math.ceil(props.options?.length / 2)).map (option => (
                                <div className="mb-1">
                                    <input type="radio" id={option} name="Selection" value={option} className={`radio ${props.id}`}/>
                                    <p className="inline ml-3">{option}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                }
            </form>
		</div>
  	)
}

export default GenericRadioSelect