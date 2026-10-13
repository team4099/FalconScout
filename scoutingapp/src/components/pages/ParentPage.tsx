import React from "react"
import { Link } from "react-router-dom";
import {DarkButton} from "../buttons";

interface ParentPageSetup {
    pageSetup: any;
}

export function ParentPage(props: ParentPageSetup){

    return (
        <div className="mx-4 pt-8 pb-10 max-w-[40rem] md:mx-auto">
            <div className="h-10 w-full mt-8 mb-8 gap-x-2">
                <h1 className="text-3xl font-bold mb-8 inline float-left">FalconScout</h1>
                <Link className="text-xl font-semibold mb-8 inline float-left m-4 -mt-1 bg-[var(--light-gray)] rounded-md p-2" to="/saved">Saved Codes</Link>
                <DarkButton/>
            </div>
            {
                props?.pageSetup?.map((page: any, key: number) => {
                    return (
                        <Link to={'/'+page.name.replaceAll(/\s/g,'')} className="text-2xl" key={key}>
                            <div className="mb-4 w-full block max-w-sm p-6 border border-[var(--light-gray)] rounded-lg shadow-sm hover:bg-[var(--hover)]">
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