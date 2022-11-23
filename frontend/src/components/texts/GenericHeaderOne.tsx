import { ComponentSetup } from "../interface"

function GenericHeaderOne(props: ComponentSetup) {

    return (
		<div className="mx-3 my-3">
			<h1 className="text-3xl font-bold">
                {props.text}
            </h1>
		</div>
  	)
}

export default GenericHeaderOne