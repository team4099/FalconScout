import React from "react"
import { Link } from "react-router-dom";

interface ParentPageSetup {
    pageSetup: any;
}

export function ParentPage(props: ParentPageSetup){

    return (
        <div className="mx-4 pt-8 pb-10 max-w-[40rem] md:mx-auto">
            <div className="h-10 w-full mb-8">
                <h1 className="text-3xl font-bold mb-8 inline float-left">FalconScout</h1>
                <Link className="text-xl font-semibold mb-8 inline float-left ml-4 -mt-1 bg-gray-200 rounded-md p-2" to="/saved">Saved Codes</Link>
            </div>
            {
                props?.pageSetup?.map((page: any) => {
                    return (
                        <Link to={'/'+page.name.replaceAll(/\s/g,'')} className="text-2xl">
                            <div className="mb-4 w-full block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100">
                                <h1 className="text-2xl font-bold mb-4">{page.name}</h1>
                                <h1 className="text-lg font-regular mb-2">{page.description}</h1>
                            </div>
                        </Link>
                    )
                })
            }
        </div>
    )
}