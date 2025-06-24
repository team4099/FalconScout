import React from "react"
import { Link } from "react-router-dom"
import { DarkButton } from "../buttons"
import { DropdownTextInput, GenericTextArea, GenericTextInput, IncrementNumberInput, SliderInput, ConeCubeIncrementInput } from "../inputs"
import {ImportedComponentSetup, PageSetup} from "../interface"
import { GenericCheckboxSelect, GenericDropdown, GenericRadioSelect, GenericToggle, ChargedUpGridSelect } from "../selects"
import { GenericHeaderOne, GenericHeaderTwo, QRCodeModal, Timer } from "../texts"
import { CycleCounter } from "../monitor"
import { RobotImage } from "../img"
import ChargedUpStartingPosition from "../selects/ChargedUpStartingPosition"

export function Page({ components, exports }: PageSetup) {
    const ComponentLibrary: { [key: string]: [React.ComponentType<any>, any] } = {
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
        "GenericHeaderTwo": [GenericHeaderTwo, ""],
        "CycleCounter": [CycleCounter, ""],
        "Timer": [Timer, ""],
        "ChargedUpGridSelect": [ChargedUpGridSelect, []],
        "ChargedUpStartingPosition": [ChargedUpStartingPosition, ""],
        "ConeCubeIncrementInput": [ConeCubeIncrementInput, []],
        "RobotImage": [RobotImage, <></>]
    }

    const componentSetup: { [key: string]: any } = {}
    const requiredComponents: string[] = [];

    components.map((component: ImportedComponentSetup) => {
        if (component.type != "Spacing") {
            try {
                componentSetup[component.id] = ComponentLibrary[component.type][1]
                if (component.required == true) {
                    requiredComponents.push(component.id)
                }
            } catch { } // Illegal component
        }
    })

    componentSetup["export"] = {
        text: "",
        delimiter: exports.delimiter,
        isRequiredCompleted: false
    }

    const propsSetPageComponent = () => {
        // if qr code has been selected to be shown
        if (componentSetup["result"]) {
            // combine all the data with the delimiter between each data point
            let order = ""
            for (let i = 0; i < exports.order.length; i++) {
                order += componentSetup[exports.order[i]]
                if (i != exports.order.length - 1) {
                    order += exports.delimiter
                }
            }
            componentSetup["export"].text = order
        }

        componentSetup["export"].isRequiredCompleted = true
        requiredComponents?.map((requiredId: string) => {
            if (["", []].includes(componentSetup[requiredId])) {
                componentSetup["export"].isRequiredCompleted = false
            }
        })
        
        console.log("Required done", componentSetup["export"].isRequiredCompleted)
    }

    return (
        <div className="mx-2 pt-8 pb-10 max-w-[40rem] md:mx-auto overscroll-none">
            <Link to="/">
                <div className="w-full h-6 mx-4 text-2xl font-bold">
                    <svg xmlns="http://www.w3.org/2000/svg" height="40" width="40" viewBox="0 0 75 75">
                        <path d="M20 44 0 24 20 4l2.8 2.85L5.65 24 22.8 41.15Z" />
                    </svg>
                </div>
            </Link>
            {
                components.map((component: ImportedComponentSetup, key: number) => {
                    if (component.type == "Spacing") {
                        return (
                            <div key={key} className="h-[2px]" />
                        )
                    }
                    else {
                        const sendprops = {
                            text: component.text,
                            route: component.route,
                            options: component.options,
                            placeholder: component.placeholder,
                            required: component.required
                        }

                        const FoundComponent: React.ComponentType<any> = ComponentLibrary[component.type][0];

                        return (
                            <FoundComponent {...sendprops} key={key} getValue={componentSetup} setValue={propsSetPageComponent} id={component.id} />
                        );

                    }
                })
            }
            <QRCodeModal getValue={componentSetup} setValue={propsSetPageComponent} required={requiredComponents} />
        </div>
    )
}
