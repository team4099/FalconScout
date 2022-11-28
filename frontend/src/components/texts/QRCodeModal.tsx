import React, { useEffect, useState } from "react"
import { ComponentSetup } from "../interface"
import QRCode from 'react-qr-code'

export function QRCodeModal(props: ComponentSetup){
    const [componentInside, setComponentInside] = useState(<></>)

    useEffect(() => {
        const interval = setInterval(() => {
            if (props.getValue.result == true){
                setComponentInside(
                    <div className={`mx-2 ml-3 border-2 rounded-lg p-4`}>
                        <h1 className="text-xl font-semibold mb-2">QR Code</h1>
                        <QRCode
                            size={256}
                            style={{ height: "auto", maxWidth: "200px", width: "200px" }}
                            value={props.getValue["export"]}
                            viewBox={`0 0 256 256`}
                            className="h-[200px] w-[200px] mx-auto mb-4"
                        />
                        <p className="text-lg">{props.getValue["export"]}</p>
                    </div>
                )
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