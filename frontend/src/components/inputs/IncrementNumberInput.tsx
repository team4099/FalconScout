import { useState } from "react";
import { ComponentSetup } from "../interface";

function IncrementNumberInput(props: ComponentSetup) {

    const [counter, setCounter] = useState(0)

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                { props.text }
            </label>
            <div className="h-14 border border-color-[#D0D5DD] border-[1.5px] rounded-xl">
                <button
                    type="button"
                    className="w-1/3 text-white h-full text-3xl rounded-l-xl float-left bg-[#cc2936]"
                    onClick={function () {if (counter > 0) {setCounter(counter-1)}}}
                >
                    -
                </button>
                <div className="flex w-1/3 h-full text-2xl float-left items-center">
                    <p className="text-center w-full">{counter}</p>
                </div>
                <button
                    type="button"
                    className="text-3xl text-white w-1/3 h-full rounded-r-xl float-right bg-[#00a676]"
                    onClick={function () {setCounter(counter+1)}}
                >
                    +
                </button>
            </div>
        </div>
    )
}

export default IncrementNumberInput