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
            <label className="block text-sm mb-2">
                { props.text }
            </label>
            <div className="h-14">
                <button
                    type="button"
                    className="w-1/3 text-[var(--default-deep-red)] h-full text-5xl float-left bg-[var(--default-pale-red)] rounded-r-none"
                    onClick={function () {if (counter > 0) {setCounter(counter-1); updateStateText(counter-1)}}}
                >
                    -
                </button>
                <div className={`flex w-1/3 h-full text-2xl float-left items-center`} style={{ backgroundColor: color == "white" ? "white" : `var(--default-deep-${color})` }}>
                    <p className={"text-center w-full"}>{counter}</p>
                </div>
                <button
                    type="button"
                    className="text-5xl text-[var(--default-deep-green)] w-1/3 h-full rounded-r-xl float-right bg-[var(--default-pale-green)] rounded-l-none"
                    onClick={function () {setCounter(counter+1); updateStateText(counter+1)}}
                >
                    +
                </button>
            </div>
        </div>
    )
}

export default IncrementNumberInput
