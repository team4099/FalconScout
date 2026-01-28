import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { BrowserRouter, HashRouter } from 'react-router-dom';
import registerServiceWorker from './registerServiceWorker';
import { ThemeProvider } from './components/ThemeContext';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
<HashRouter>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </HashRouter>
)

registerServiceWorker();