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

import IDS from './pages/IDS';
import GiorgioPage from './pages/GiorgioPage';
import FerraPage from './pages/FerraPage';
import ParsaPage from './pages/ParsaPage';

import TimeControlbar from './components/TimeControlbar/TimeControlbar';

function App() {
  return (
    <div className="App h-100">
      <TimeControlbar/>
      <Router>
        <nav>
          <ul>
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/">Dashboard</Link>
            </li>
            
            {/*
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Ferra">Ferra</Link>
            </li>
            */}
            
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Parsa">FIREWALL_Time</Link>
            </li>

            
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/Giorgio">Firewall_categories</Link>
            </li>
            
            <li style={{ display: 'inline', marginRight: '10px' }}>
              <Link to="/IDS">IDS_Time</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/Ferra" element={<FerraPage/>}/>
          <Route path="/Parsa" element={<ParsaPage/>}/>
          <Route path="/Giorgio" element={<GiorgioPage/>}/>
          <Route path="/IDS" element={<IDS/>}/>
          <Route path="/" element={<DashboardPage/>}/>
        </Routes>

      </Router>
    </div>
  );
}

export default App;
