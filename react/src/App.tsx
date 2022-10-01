import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { DropdownTextInput, GenericTextInput } from "./components/inputs"


function App() {
	return (
		<div>
			<GenericTextInput/>
			<DropdownTextInput/>
		</div>
	)
}

export default App
