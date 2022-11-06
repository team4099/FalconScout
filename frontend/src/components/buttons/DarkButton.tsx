interface ButtonSetup {
	text: string;
	route: string;
}

function DarkButton(props: ButtonSetup) {

    return (
    
		<div className="mx-3 my-3">
			<button className="bg-black text-sm font-semibold outline w-full hover:outline-3 hover:outline-gray-300 text-white py-2 px-2 rounded-lg">
                { props.text }
            </button>
		</div>

  	)
}

export default DarkButton
