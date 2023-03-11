import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { BrowserRouter, HashRouter } from 'react-router-dom';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
<HashRouter>
    <App />
  </HashRouter>
)

registerServiceWorker();