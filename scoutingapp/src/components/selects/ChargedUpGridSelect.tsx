import { useState } from "react";
import { ComponentSetup } from "../interface";

export function ChargedUpGridSelect(props: ComponentSetup){


    const toggle = (location: any) => {
        newValues = JSON.parse(JSON.stringify(gridValues)); 
        if (location[1] == "L"){
            newValues[location] = hybridMapping[newValues[location]]
        }
        else if (["1", "3", "4", "6", "7", "9"].includes(location[0])) {
            newValues[location] = coneNodeMapping[newValues[location]]; 
        }
        else {
            newValues[location] = cubeNodeMapping[newValues[location]]; 
        }
        setGridValues(newValues)

        updateStateSelections(newValues)
    }

    const [gridState, setGridState] = useState(1);

    var values: any = {}
    const nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for (var col of nums){
        for (var row of ["L", "M", "H"]){
            values[col + row.toString()] = false
        }
    }

    var hybridMapping: any = {
        false: "cube",
        cube: "cone",
        cone: "supercharge",
        supercharge: false
    }

    var coneNodeMapping: any = {
        false: "cone",
        cone: "supercharge",
        supercharge: false
    }

    var cubeNodeMapping: any = {
        false: "cube",
        cube: "supercharge",
        supercharge: false
    }

    const [gridValues, setGridValues] = useState(values)
    var newValues = gridValues

    console.log(gridValues)

    const updateStateSelections = (newValues: any) => {
		var state = props.getValue

        var values = Array()
        
        for (const check of Object.keys(newValues)) {
            if (check[1] == 'L'){
                console.log(check, newValues[check])
                if (newValues[check] == "cone" || newValues[check] == "cube"){
                    values.push(check + newValues[check])
                }
            }
            else if (newValues[check] == "cube" || newValues[check] == "cone") {
                values.push(check)
            }
            else if (newValues[check] == "supercharge"){
                values.push(check)
                values.push(check)
            }
        }

		state[props.id] = values
		props.setValue(state)
	}

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                {props.text}
            </label>
            {gridState == 1 && (
                <ul className="flex flex-wrap text-sm font-medium text-center text-gray-500 border-b border-gray-200">
                    <li className="mr-2" onClick={() => {setGridState(1)}}>
                        <a aria-current="page" className="inline-block p-4 text-black bg-gray-100 rounded-t-lg active">Left</a>
                    </li>
                    <li className="mr-2" onClick={() => {setGridState(2)}}>
                        <a className="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50">Coop</a>
                    </li>
                    <li className="mr-2" onClick={() => {setGridState(3)}}>
                        <a className="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50">Right</a>
                    </li>
                </ul>
            )}
            {gridState == 2 && (
                <ul className="flex flex-wrap text-sm font-medium text-center text-gray-500 border-b border-gray-200">
                    <li className="mr-2" onClick={() => {setGridState(1)}}>
                        <a className="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50">Left</a>
                    </li>
                    <li className="mr-2" onClick={() => {setGridState(2)}}>
                        <a aria-current="page" className="inline-block p-4 text-black bg-gray-100 rounded-t-lg active">Coop</a>
                    </li>
                    <li className="mr-2" onClick={() => {setGridState(3)}}>
                        <a className="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50">Right</a>
                    </li>
                </ul>
            )}
            {gridState == 3 && (
                <ul className="flex flex-wrap text-sm font-medium text-center text-gray-500 border-b border-gray-200">
                    <li className="mr-2" onClick={() => {setGridState(1)}}>
                        <a className="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50">Left</a>
                    </li>
                    <li className="mr-2" onClick={() => {setGridState(2)}}>
                        <a className="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50">Coop</a>
                    </li>
                    <li className="mr-2" onClick={() => {setGridState(3)}}>
                        <a aria-current="page" className="inline-block p-4 text-black bg-gray-100 rounded-t-lg active">Right</a>
                    </li>
                </ul>
            )}
            {gridState == 1 && (
                <div className="flex flex-col gap-2">
                    <div className="flex flex-row gap-2">
                        {gridValues["1H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("1H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1H</h1>
                            </div>
                        )}
                        {gridValues["1H"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("1H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1H</h1>
                            </div>
                        )}
                        {gridValues["1H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("1H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1H</h1>
                            </div>
                        )}
                        {gridValues["2H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-100" onClick={() => {toggle("2H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2H</h1>
                            </div>
                        )}
                        {gridValues["2H"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("2H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2H</h1>
                            </div>
                        )}
                        {gridValues["2H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("2H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2H</h1>
                            </div>
                        )}
                        {gridValues["3H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("3H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3H</h1>
                            </div>
                        )}
                        {gridValues["3H"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("3H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3H</h1>
                            </div>
                        )}
                        {gridValues["3H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("3H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3H</h1>
                            </div>
                        )}
                    </div>
                    <div className="flex flex-row gap-2">
                        {gridValues["1M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("1M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1M</h1>
                            </div>
                        )}
                        {gridValues["1M"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("1M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1M</h1>
                            </div>
                        )}
                        {gridValues["1M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("1M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1M</h1>
                            </div>
                        )}
                        {gridValues["2M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-100" onClick={() => {toggle("2M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2M</h1>
                            </div>
                        )}
                        {gridValues["2M"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("2M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2M</h1>
                            </div>
                        )}
                        {gridValues["2M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("2M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2M</h1>
                            </div>
                        )}
                        {gridValues["3M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("3M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3M</h1>
                            </div>
                        )}
                        {gridValues["3M"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("3M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3M</h1>
                            </div>
                        )}
                        {gridValues["3M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("3M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3M</h1>
                            </div>
                        )}
                    </div>
                    <div className="flex flex-row gap-2">
                        {gridValues["1L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("1L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1L</h1>
                            </div>
                        )}
                        {gridValues["1L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("1L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1L</h1>
                            </div>
                        )}
                        {gridValues["1L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("1L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1L</h1>
                            </div>
                        )}
                        {gridValues["1L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("1L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">1L</h1>
                            </div>
                        )}
                        {gridValues["2L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("2L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2L</h1>
                            </div>
                        )}
                        {gridValues["2L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("2L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2L</h1>
                            </div>
                        )}
                        {gridValues["2L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("2L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2L</h1>
                            </div>
                        )}
                        {gridValues["2L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("2L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">2L</h1>
                            </div>
                        )}
                        {gridValues["3L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("3L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3L</h1>
                            </div>
                        )}
                        {gridValues["3L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("3L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3L</h1>
                            </div>
                        )}
                        {gridValues["3L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("3L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3L</h1>
                            </div>
                        )}
                        {gridValues["3L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("3L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">3L</h1>
                            </div>
                        )}
                    </div>
                </div>
            )}
            {gridState == 2 && (
                <div className="flex flex-col gap-2">
                    <div className="flex flex-row gap-2">
                        {gridValues["4H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("4H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4H</h1>
                            </div>
                        )}
                        {gridValues["4H"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("4H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4H</h1>
                            </div>
                        )}
                        {gridValues["4H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("4H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4H</h1>
                            </div>
                        )}
                        {gridValues["5H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-100" onClick={() => {toggle("5H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5H</h1>
                            </div>
                        )}
                        {gridValues["5H"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("5H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5H</h1>
                            </div>
                        )}
                        {gridValues["5H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("5H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5H</h1>
                            </div>
                        )}
                        {gridValues["6H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("6H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6H</h1>
                            </div>
                        )}
                        {gridValues["6H"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("6H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6H</h1>
                            </div>
                        )}
                        {gridValues["6H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("6H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6H</h1>
                            </div>
                        )}
                    </div>
                    <div className="flex flex-row gap-2">
                        {gridValues["4M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("4M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4M</h1>
                            </div>
                        )}
                        {gridValues["4M"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("4M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4M</h1>
                            </div>
                        )}
                        {gridValues["4M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("4M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4M</h1>
                            </div>
                        )}
                        {gridValues["5M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-100" onClick={() => {toggle("5M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5M</h1>
                            </div>
                        )}
                        {gridValues["5M"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("5M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5M</h1>
                            </div>
                        )}
                        {gridValues["5M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("5M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5M</h1>
                            </div>
                        )}
                        {gridValues["6M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("6M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6M</h1>
                            </div>
                        )}
                        {gridValues["6M"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("6M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6M</h1>
                            </div>
                        )}
                        {gridValues["6M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("6M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6M</h1>
                            </div>
                        )}
                    </div>
                    <div className="flex flex-row gap-2">
                        {gridValues["4L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("4L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4L</h1>
                            </div>
                        )}
                        {gridValues["4L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("4L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4L</h1>
                            </div>
                        )}
                        {gridValues["4L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("4L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4L</h1>
                            </div>
                        )}
                        {gridValues["4L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("4L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">4L</h1>
                            </div>
                        )}
                        {gridValues["5L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("5L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5L</h1>
                            </div>
                        )}
                        {gridValues["5L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("5L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5L</h1>
                            </div>
                        )}
                        {gridValues["5L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("5L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5L</h1>
                            </div>
                        )}
                        {gridValues["5L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("5L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">5L</h1>
                            </div>
                        )}
                        {gridValues["6L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("6L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6L</h1>
                            </div>
                        )}
                        {gridValues["6L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("6L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6L</h1>
                            </div>
                        )}
                        {gridValues["6L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("6L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6L</h1>
                            </div>
                        )}
                        {gridValues["6L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("6L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">6L</h1>
                            </div>
                        )}
                    </div>
                </div>
            )}
            {gridState == 3 && (
                <div className="flex flex-col gap-2">
                    <div className="flex flex-row gap-2">
                        {gridValues["7H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("7H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7H</h1>
                            </div>
                        )}
                        {gridValues["7H"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("7H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7H</h1>
                            </div>
                        )}
                        {gridValues["7H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("7H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7H</h1>
                            </div>
                        )}
                        {gridValues["8H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-100" onClick={() => {toggle("8H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8H</h1>
                            </div>
                        )}
                        {gridValues["8H"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("8H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8H</h1>
                            </div>
                        )}
                        {gridValues["8H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("8H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8H</h1>
                            </div>
                        )}
                        {gridValues["9H"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("9H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9H</h1>
                            </div>
                        )}
                        {gridValues["9H"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("9H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9H</h1>
                            </div>
                        )}
                        {gridValues["9H"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("9H")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9H</h1>
                            </div>
                        )}
                    </div>
                    <div className="flex flex-row gap-2">
                        {gridValues["7M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("7M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7M</h1>
                            </div>
                        )}
                        {gridValues["7M"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("7M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7M</h1>
                            </div>
                        )}
                        {gridValues["7M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("7M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7M</h1>
                            </div>
                        )}
                        {gridValues["8M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-100" onClick={() => {toggle("8M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8M</h1>
                            </div>
                        )}
                        {gridValues["8M"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("8M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8M</h1>
                            </div>
                        )}
                        {gridValues["8M"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("8M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8M</h1>
                            </div>
                        )}
                        {gridValues["9M"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-100" onClick={() => {toggle("9M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9M</h1>
                            </div>
                        )}
                        {gridValues["9M"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("9M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9M</h1>
                            </div>
                        )}
                        {gridValues["9M"] == true && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("9M")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9M</h1>
                            </div>
                        )}
                    </div>
                    <div className="flex flex-row gap-2">
                        {gridValues["7L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("7L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7L</h1>
                            </div>
                        )}
                        {gridValues["7L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("7L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7L</h1>
                            </div>
                        )}
                        {gridValues["7L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("7L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7L</h1>
                            </div>
                        )}
                        {gridValues["7L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("7L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">7L</h1>
                            </div>
                        )}
                        {gridValues["8L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("8L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8L</h1>
                            </div>
                        )}
                        {gridValues["8L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("8L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8L</h1>
                            </div>
                        )}
                        {gridValues["8L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("8L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8L</h1>
                            </div>
                        )}
                        {gridValues["8L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("8L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">8L</h1>
                            </div>
                        )}
                        {gridValues["9L"] == false && (
                            <div className="basis-1/3 rounded-lg h-24 bg-gray-100" onClick={() => {toggle("9L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9L</h1>
                            </div>
                        )}
                        {gridValues["9L"] == "cone" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-yellow-300" onClick={() => {toggle("9L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9L</h1>
                            </div>
                        )}
                        {gridValues["9L"] == "cube" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-purple-300" onClick={() => {toggle("9L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9L</h1>
                            </div>
                        )}
                        {gridValues["9L"] == "supercharge" && (
                            <div className="basis-1/3 rounded-lg h-24 bg-pink-400" onClick={() => {toggle("9L")}}>
                                <h1 className="text-2xl font-bold text-center mt-8 select-none">9L</h1>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}