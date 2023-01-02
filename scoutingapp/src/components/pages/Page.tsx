import React from "react"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { DarkButton } from "../buttons"
import { DropdownTextInput, GenericTextArea, GenericTextInput, IncrementNumberInput, SliderInput } from "../inputs"
import { ComponentSetup, PageSetup } from "../interface"
import { GenericCheckboxSelect, GenericDropdown, GenericRadioSelect, GenericToggle } from "../selects"
import { GenericHeaderOne, GenericHeaderTwo, QRCodeModal } from "../texts"

interface ImportedComponentSetup extends ComponentSetup {
    type: string;
}

export function Page(props: PageSetup){
    const ComponentLibrary: Object = {
        "DarkButton": [DarkButton, false],
        "DropdownTextInput": [DropdownTextInput, ["", ""]],
        "GenericTextArea": [GenericTextArea, ""],
        "GenericTextInput": [GenericTextInput, ""],
        "IncrementNumberInput": [IncrementNumberInput, 0],
        "SliderInput": [SliderInput, 0],
        "GenericCheckboxSelect": [GenericCheckboxSelect, []],
        "GenericDropdown": [GenericDropdown, ""],
        "GenericRadioSelect": [GenericRadioSelect, ""],
        "GenericToggle": [GenericToggle, false],
        "GenericHeaderOne": [GenericHeaderOne, ""],
        "GenericHeaderTwo": [GenericHeaderTwo, ""]
    }

    let componentSetup: any = {}

    props?.config?.components?.map((component: ImportedComponentSetup) => {
        if (component.type != "Spacing"){
            try {
                componentSetup[component.id] = (ComponentLibrary as any)[component.type][1]
            } catch {}
        }
    })

    componentSetup["export"] = {
        text: "",
        delimiter: props?.config?.export.delimiter
    }

    const [pageComponents, setPageComponents] = useState(componentSetup)
    const propsSetPageComponent = (state: any) => {
        setPageComponents(state)
        componentSetup = pageComponents
        if (pageComponents["result"]){
            var order = ""
            for (var i = 0; i < props?.config?.export.order.length; i++){
                order += pageComponents[props?.config?.export.order[i]]
                if (i != props?.config?.export.order.length - 1){
                    order += props?.config?.export.delimiter
                }
            }
            componentSetup["export"].text = order
            setPageComponents(componentSetup)
        }
    }

    return (
        <div className="mx-2 pt-8 pb-10 max-w-[40rem] md:mx-auto">
            <Link to="/">
                <div className="w-full h-6 mx-4 text-2xl font-bold">
                    <svg xmlns="http://www.w3.org/2000/svg" height="40" width="40" viewBox="0 0 75 75">
                        <path d="M20 44 0 24 20 4l2.8 2.85L5.65 24 22.8 41.15Z"/>
                    </svg>
                </div>
            </Link>
            {
                props?.config?.components?.map((component: ImportedComponentSetup) => {
                    if (component.type == "Spacing"){
                        return (
                            <div className="h-[1px]"/>
                        )
                    }
                    else {
                        var sendprops = {
                            text: component.text,
                            route: component.route,
                            options: component.options,
                            placeholder: component.placeholder
                        }

                        const FoundComponent = (ComponentLibrary as any)[component.type][0];

                        return (
                            <FoundComponent {...sendprops} getValue={pageComponents} setValue={propsSetPageComponent} id={component.id}/>
                        );

                    }
                })
            }
            <QRCodeModal getValue={pageComponents} setValue={propsSetPageComponent}/>
        </div>
    )
}