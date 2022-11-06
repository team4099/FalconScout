import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { DropdownTextInput, GenericTextInput } from "./components/inputs"
import { GenericTextArea } from "./components/inputs"
import { DarkButton } from "./components/buttons"


function App() {
  return (
    <div>
      <div>
        <GenericTextInput/>
        <DropdownTextInput/>
        <GenericTextArea/>
      </div>
      <div>
        <DarkButton text="Submit" route="todo"/>
      </div>
    </div>
  )
}

export default App
