import React from "react"
import { useState } from "react";
import { ComponentSetup } from "../interface";

function IncrementNumberInput(props: ComponentSetup) {

    const [counter, setCounter] = useState(0)

    const color = props?.options?.[0]

    const updateStateText = (value: any) => {
		//console.log(props.getValue)
		var state = props.getValue
		state[props.id] = value
		props.setValue(state)
	}

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                { props.text }
            </label>
            <div className="h-14 border border-color-[#D0D5DD] border-[1.5px] rounded-xl">
                <button
                    type="button"
                    className="w-1/3 text-[#cc2936] h-full text-5xl rounded-l-xl float-left bg-[#FDE7E7]"
                    onClick={function () {if (counter > 0) {setCounter(counter-1); updateStateText(counter-1)}}}
                >
                    -
                </button>
                <div className={`flex w-1/3 h-full text-2xl float-left items-center ${color == "red" ? "bg-red-400" : color == "yellow" ? "bg-amber-300" : color == "blue" ? "bg-blue-500" : color == "green" ? "bg-green-400" : "bg-white"}`}>
                    <p className={"text-center w-full"}>{counter}</p>
                </div>
                <button
                    type="button"
                    className="text-5xl text-[#18611B] w-1/3 h-full rounded-r-xl float-right bg-[#E2F8E3]"
                    onClick={function () {setCounter(counter+1); updateStateText(counter+1)}}
                >
                    +
                </button>
            </div>
        </div>
    )
}

export default IncrementNumberInput
