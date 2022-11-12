import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { DropdownTextInput, GenericTextInput, SliderInput } from "./components/inputs"
import { GenericTextArea } from "./components/inputs"
import { DarkButton } from "./components/buttons"
import IncrementNumberInput from './components/inputs/IncrementNumberInput'
import GenericDropdown from './components/selects/GenericDropdown'


function App() {
  return (
    <div>
      <div>
        <GenericTextInput text="Username" placeholder={["pranav"]}/>
        <DropdownTextInput text="Match" options={["qm", "qf", "sf", "f"]} placeholder={["10"]} route="todo"/>
        <GenericTextArea text="Username" placeholder={["pranav"]}/>
        <IncrementNumberInput text="Teleop Upper Scored"/>
        <SliderInput text="Driver Rating" options={["0", "10"]}/>
      </div>
      <div>
        <GenericDropdown text="Zones" options={["tarmac", "fender", "hangar", "terminal"]}/>
      </div>
      <div>
        <DarkButton text="Submit" route="todo"/>
      </div>
    </div>
  )
}

export default App
