import Home from './components/Home'
import { BrowserRouter as Router , Routes , Route } from 'react-router-dom';
import Recpie from './components/Recpie';
import { defineConfig } from 'vite';

// https://vitejs.dev/config/

function App() {
  
  return (
    <Router>
    <Routes>
      <Route path="/" element={<Home />} ></Route>
      <Route path="/recpie" element={<Recpie />}></Route>
    </Routes>
    </Router>
  )
}

export default App
