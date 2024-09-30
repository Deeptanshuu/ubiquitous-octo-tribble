import Home from './components/Home'
import { BrowserRouter as Router , Routes , Route } from 'react-router-dom';
import Recpie from './components/Recpie';
import Loading from './components/Loading';

function App() {
  
  return (
    <Router>
    <Routes>
      <Route path="/" element={<Home />} ></Route>
      <Route path="/recpie" element={<Recpie />}></Route>
      <Route path="/loading" element={<Loading />}></Route> 
    </Routes>
    </Router>
  )
}

export default App
