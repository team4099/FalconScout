import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import { GenericTextInput } from "./components/inputs"
import { GenericTextArea } from "./components/inputs"


function App() {
  return (
    <div>
      <GenericTextInput/>
      <GenericTextArea/>
    </div>
  )
}

export default App
