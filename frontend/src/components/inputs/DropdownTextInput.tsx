function DropdownTextInput() {

    return (
        <div className="mx-3 mb-8">
            <label className="block text-[#344054] text-sm mb-2">
                Match Number
            </label>
            <div className="flex appearance-none h-[40px] border border-color-[#D0D5DD] border-[1.5px] rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                <select name="cars" id="cars" className="inline">
                    <option value="volvo">Volvo</option>
                    <option value="saab">Saab</option>
                    <option value="mercedes">Mercedes</option>
                    <option value="audi">Audi</option>
                </select>

                <input className="text-black pl-4 focus:outline-none inline flex-grow w-full">
                </input>
            </div>
        </div>
    )
}
  
export default DropdownTextInput
  