function GenericTextInput() {

    return (
    
		<div className="mx-3 my-3">
			<label className="block text-[#344054] text-sm mb-2">
				Your message
			</label>
			<input className="appearance-none border border-color-[#D0D5DD] rounded w-full py-2 px-3 text-gray-700 focus:outline-none" id="username" type="text" placeholder="Username"></input>
		</div>

  	)
}

export default GenericTextInput
