import { ComponentSetup } from "../interface"

function DropdownTextInput(props: ComponentSetup) {

    return (
        <div className="mx-3 my-3">
            <label className="block text-[#344054] text-sm mb-2">
                { props.text }
            </label>
            <div className="flex appearance-none h-[40px] border border-color-[#D0D5DD] border-[1.5px] rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                <select name="option" id="options" className="inline">
                    { props.options?.map (option => (
                        <option value={option}>{option}</option>
                    ))}
                </select>

                <input className="text-black pl-4 focus:outline-none inline flex-grow w-full" placeholder={props.placeholder[0]}>
                </input>
            </div>
        </div>
    )
}
  
export default DropdownTextInput
  