import './App.css'
import { Routes, Route } from 'react-router-dom';
import { Page, ParentPage, StoragePage } from "./components/pages"
import structure from "./config/structure.json"
import React from 'react';


function App() {
  if ([null, ""].includes(localStorage.getItem("codes"))){
    localStorage.setItem("codes", "{}")
  }

  return (
    <Routes>
      <Route path='/' element={<ParentPage pageSetup={structure}/>}></Route>
      {
        structure.map((page) => {
            return (
              <Route path={'/'+page.name.replaceAll(/\s/g,'')} element={<Page config={page}/>}></Route>
            )
        })
      }
      <Route path='/saved' element={<StoragePage/>}></Route>
    </Routes>
    
    
  )
}

export default App
