import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { DropdownTextInput, GenericTextInput } from "./components/inputs"
import { GenericTextArea } from "./components/inputs"
import { DarkButtonSmall } from "./components/buttons"
import { DarkButtonMedium } from "./components/buttons"
import { DarkButtonLarge} from "./components/buttons"


function App() {
  return (
    <div>
      <div>
        <GenericTextInput/>
        <DropdownTextInput/>
        <GenericTextArea/>
      </div>
      <div>
        <DarkButtonSmall/>
        <DarkButtonMedium/>
        <DarkButtonLarge/>
      </div>
    </div>
  )
}

export default App
