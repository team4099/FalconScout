function GenericTextArea() {

    return (
    
		<div className="mx-3 my-3">
			<label className="block mb-2 text-sm text-gray-[#344054]">Your message</label>
			<textarea id="message" className="block p-4 w-full h-40 text text-[#000000] rounded-lg border border-color-[#D0D5DD] focus:outline-none" placeholder="Your message..."></textarea>
		</div>

  	)
}

export default GenericTextArea
