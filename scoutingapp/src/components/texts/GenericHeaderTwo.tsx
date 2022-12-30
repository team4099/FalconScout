import { ComponentSetup } from "../interface"

function GenericHeaderTwo(props: ComponentSetup) {

    return (
		<div className="mx-3 my-3 mt-3">
			<h1 className="text-xl font-semibold">
                {props.text}
            </h1>
		</div>
  	)
}

export default GenericHeaderTwo