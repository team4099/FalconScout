import React, { useEffect, useState } from "react"
import { ComponentSetup } from "../interface"
import QRCode from 'react-qr-code'

export function QRCodeModal(props: ComponentSetup){
    const [componentInside, setComponentInside] = useState(<></>)
    /*
    <button onClick={addToLocalStorage} className="text-lg font-semibold mb-2 ml-2 bg-gray-200 rounded-md px-3 py-[2px] -mt-[2px]">Save</button>
    */

    const addToLocalStorage = function () {
        console.log(localStorage.getItem("codes") as string)
        var currentData = JSON.parse(localStorage.getItem("codes") as string)
        currentData[props.getValue["MatchKey"].join("")] = props.getValue["export"].text
        localStorage.setItem("codes", JSON.stringify(currentData))
    }

    useEffect(() => {
        const interval = setInterval(() => {
            var requiredFinished = true

            console.log(props.required)
            for (const id of props.required){
                console.log(props.getValue[id])
                if (["", [], ","].includes(props.getValue[id]) || 
                    (props.getValue[id][0].length == 2 && 
                        (props.getValue[id][0] == "" || props.getValue[id][1] == "")
                    )
                ){
                    requiredFinished = false
                    break
                }
            }

            if (props.getValue.result == true){
                if (requiredFinished){
                    addToLocalStorage()
                    setComponentInside(
                        <div className={`mx-2 ml-3 border-2 rounded-lg p-4`}>
                            <div className="h-12">
                                <h1 className="text-xl font-semibold mb-2 inline float-left">QR Code</h1>
                                
                            </div>
                            <QRCode
                                size={256}
                                style={{ height: "auto", maxWidth: "200px", width: "200px" }}
                                value={props.getValue["export"].text}
                                viewBox={`0 0 256 256`}
                                className="h-[200px] w-[200px] mx-auto mb-4"
                            />
                        </div>
                    )
                }
                else {
                    setComponentInside(
                        <div className="h-12 w-full px-2">
                            <div className="h-12 w-full border-4 border-red-400 rounded-lg bg-red-200 text-center pt-2 font-semibold">
                                Required Fields not finished
                            </div>
                        </div>
                    )
                }

            }
            else {
                setComponentInside(
                    <div></div>
                )
            }
        }, 200);
        return () => clearInterval(interval);
      }, []);

    const fakeIter=[""]

    return (<>
            {componentInside}
        </>
    )
}