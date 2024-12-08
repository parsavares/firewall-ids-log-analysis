import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import DashboardPage from './pages/DashboardPage';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

import YufeiPage from './pages/YufeiPage';
import GiorgioPage from './pages/GiorgioPage';
import FerraPage from './pages/FerraPage';
import ParsaPage from './pages/ParsaPage';

function App() {
  return (
    <div className="App h-100">
      <Router>
        <nav>
          <ul>
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/">Dashboard</Link>
            </li>
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Ferra">Ferra</Link>
            </li>
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Parsa">Parsa</Link>
            </li>
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Giorgio">Giorgio</Link>
            </li>
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Yufei">Yufei</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/Ferra" element={<FerraPage/>}/>
          <Route path="/Parsa" element={<ParsaPage/>}/>
          <Route path="/Giorgio" element={<GiorgioPage/>}/>
          <Route path="/Yufei" element={<YufeiPage/>}/>
          <Route path="/" element={<DashboardPage/>}/>
        </Routes>

      </Router>
    </div>
  );
}

export default App;
