import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import store from './store';
import { Provider } from 'react-redux';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    {/*<React.StrictMode>   In development mode, components are rendered 2 times.*/}
      <Provider store={store}>
        <App />
      </Provider>
    {/*</React.StrictMode>  */}
  </>
);

