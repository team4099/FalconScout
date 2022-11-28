import './App.css'
import { Routes, Route } from 'react-router-dom';
import { Page, ParentPage } from "./components/pages"
import structure from "./config/structure.json"
import React from 'react';


function App() {
  return (
    <Routes>
      <Route path='/' element={<ParentPage pageSetup={structure}/>}></Route>
      {
        structure.map((page) => {
            return (
              <Route path={'/'+page.name} element={<Page config={page}/>}></Route>
            )
        })
      }
    </Routes>
    
    
  )
}

export default App
