import React from "react"
import { Link } from "react-router-dom";
import QRCode from 'react-qr-code'

export function StoragePage() {
    return (
        <div className="mx-4 pt-8 pb-10 max-w-[40rem] md:mx-auto">
            <Link to="/">
                <div className="w-full h-6 mx-4 text-2xl font-bold">
                    <svg xmlns="http://www.w3.org/2000/svg" height="40" width="40" viewBox="0 0 75 75">
                        <path d="M20 44 0 24 20 4l2.8 2.85L5.65 24 22.8 41.15Z"/>
                    </svg>
                </div>
            </Link>
            <div className="px-4">
                <div className="h-10 w-full mb-8 mt-4">
                    <h1 className="text-3xl font-bold mb-8 inline float-left">Saved Codes</h1>
                </div>
            </div>
            <div className="mt-4 px-4">
                { Object.keys(JSON.parse(localStorage.getItem("codes") as string)).map ((option: any) => (
                    <div className="border-b-2 border-gray-700 pb-4 pt-4">
                        <h1 className="text-2xl font-bold mb-4">{option}</h1>
                        <QRCode
                            size={256}
                            style={{ height: "auto", maxWidth: "200px", width: "200px"}}
                            value={JSON.parse(localStorage.getItem("codes") as string)[option]}
                            viewBox={`0 0 256 256`}
                            className="h-[200px] w-[200px] mx-auto mb-4"
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}