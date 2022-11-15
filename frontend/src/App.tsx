import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { DropdownTextInput, GenericTextInput, SliderInput, GenericTextArea, IncrementNumberInput } from "./components/inputs"
import { DarkButton } from "./components/buttons"
import { GenericDropdown, GenericMultiDropdown, GenericToggle } from './components/selects'


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
        <GenericMultiDropdown text="Zones" options={["tarmac", "fender", "hangar", "terminal"]}/>
        <GenericToggle text="Taxied"/>
      </div>
      <div>
        <DarkButton text="Submit" route="todo"/>
      </div>
    </div>
  )
}

export default App
