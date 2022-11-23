import { JSXElementConstructor } from "react"
import { DarkButton } from "../buttons"
import { DropdownTextInput, GenericTextArea, GenericTextInput, IncrementNumberInput, SliderInput } from "../inputs"
import { ComponentSetup, PageSetup } from "../interface"
import { GenericCheckboxSelect, GenericDropdown, GenericRadioSelect, GenericToggle } from "../selects"
import { GenericHeaderOne, GenericHeaderTwo } from "../texts"

interface ImportedComponentSetup extends ComponentSetup {
    type: string;
}

export function Page(props: PageSetup){
    console.log(props?.config)
    const ComponentLibrary: Object = {
        "DarkButton": DarkButton,
        "DropdownTextInput": DropdownTextInput,
        "GenericTextArea": GenericTextArea,
        "GenericTextInput": GenericTextInput,
        "IncrementNumberInput": IncrementNumberInput,
        "SliderInput": SliderInput,
        "GenericCheckboxSelect": GenericCheckboxSelect,
        "GenericDropdown": GenericDropdown,
        "GenericRadioSelect": GenericRadioSelect,
        "GenericToggle": GenericToggle,
        "GenericHeaderOne": GenericHeaderOne,
        "GenericHeaderTwo": GenericHeaderTwo
    }

    return (
        <div className="mx-2 pt-8 pb-10 max-w-[40rem] md:mx-auto">
            {
                props?.config?.components?.map((component: ImportedComponentSetup) => {
                    if (component.type == "Spacing"){
                        return (
                            <div className="h-[1px]"/>
                        )
                    }
                    else {
                        const sendprops = {
                            text: component.text,
                            route: component.route,
                            options: component.options,
                            placeholder: component.placeholder,

                        }

                        var FoundComponent = (ComponentLibrary as any)[component.type];

                        return (
                            <FoundComponent {...sendprops}/>
                        );

                    }
                })
            }
        </div>
    )
}