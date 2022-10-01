import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { DropdownTextInput, GenericTextInput } from "./components/inputs"
import { GenericTextArea } from "./components/inputs"


function App() {
  return (
    <div>
      <GenericTextInput/>
	  <DropdownTextInput/>
      <GenericTextArea/>
    </div>
  )
}

export default App
