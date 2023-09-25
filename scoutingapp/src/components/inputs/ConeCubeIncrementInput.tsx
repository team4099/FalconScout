import React from "react"
import { useState } from "react";
import { ComponentSetup } from "../interface";

function ConeCubeIncrementInput(props: ComponentSetup) {

    const [coneCounter, setConeCounter] = useState(0)
    const [cubeCounter, setCubeCounter] = useState(0)

    const color = props?.options?.[0]

    const updateStateText = (values: any) => {
		var state = props.getValue


		state[props.id] = values
		props.setValue(state)
	}

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                { props.text }
            </label>
            <div className="flex justify-between"> 
                <div className="w-[45%] h-16 border border-color-[#D0D5DD] border-[1.5px] rounded-xl">
                    <button
                        type="button"
                        className="w-1/3 text-[#cc2936] h-full text-5xl rounded-l-xl float-left bg-[#FDE7E7]"
                        onClick={function () {if (coneCounter > 0) {setConeCounter(coneCounter-1); updateStateText([coneCounter-1, cubeCounter])}}}
                    >
                        -
                    </button>
                    <div className={`flex w-1/3  h-full text-2xl float-left items-center ${color == "red" ? "bg-red-400" : color == "yellow" ? "bg-amber-300" : color == "green" ? "bg-green-400" : "bg-white"}`}>
                        <p className={"text-center text-white  font-semibold flex items-center pt-1 justify-center text-md h-[80%] w-full  bg-center bg-[url('../public/coneSprite.svg')] bg-contain bg-no-repeat"}>{coneCounter}</p>
                    </div>
                    <button
                        type="button"
                        className="text-5xl text-[#18611B] w-1/3 h-full rounded-r-xl float-right bg-[#E2F8E3]"
                        onClick={function () {setConeCounter(coneCounter+1); updateStateText([coneCounter+1, cubeCounter])}}
                    >
                        +
                    </button>
                </div>
                <div className="w-[45%] h-16 border border-color-[#D0D5DD] border-[1.5px] rounded-xl">
                    <button
                        type="button"
                        className="w-1/3 text-[#cc2936] h-full text-5xl rounded-l-xl float-left bg-[#FDE7E7]"
                        onClick={function () {if (cubeCounter > 0) {setCubeCounter(cubeCounter-1); updateStateText([coneCounter, cubeCounter-1])}}}
                    >
                        -
                    </button>
                    <div className={`flex w-1/3  h-full text-2xl float-left items-center ${color == "red" ? "bg-red-400" : color == "yellow" ? "bg-amber-300" : color == "green" ? "bg-green-400" : "bg-white"}`}>
                        <p className={"text-center text-white font-semibold flex items-center pt-1 justify-center text-md h-[80%] w-full  bg-center bg-[url('../public/cubeSprite.svg')] bg-contain bg-no-repeat"}>{cubeCounter}</p>
                    </div>
                    <button
                        type="button"
                        className="text-5xl text-[#18611B] w-1/3 h-full rounded-r-xl float-right bg-[#E2F8E3]"
                        onClick={function () {setCubeCounter(cubeCounter+1); updateStateText([coneCounter, cubeCounter+1])}}
                    >
                        +
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ConeCubeIncrementInput