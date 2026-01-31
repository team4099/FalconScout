import './App.css'
import {Routes, Route} from 'react-router-dom';
import {Page, ParentPage, StoragePage} from "./components/pages"
import structure from "./config/structure.json"
import React from 'react';
import {PageSetup} from "./components/interface";
import Layout from './components/pages/Layout';
import {DarkButton} from "./components/buttons";


function App() {
  if ([null, ""].includes(localStorage.getItem("codes"))) {
    localStorage.setItem("codes", "{}")
  }

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<ParentPage pageSetup={structure}/>} />
        {
          structure.map((page: PageSetup, key: number) => {
              return (
                <Route key={key} path={'/'+page.name.replaceAll(/\s/g,'')} element={<Page {...page}/>}></Route>
              )
          })
        }
        <Route path='/saved' element={<StoragePage/>}></Route>
      </Route>
    </Routes>
  )
}

export default App
