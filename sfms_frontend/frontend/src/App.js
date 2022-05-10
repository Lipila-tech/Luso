import './App.css';
import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h3>Student Fees Management</h3>
        <h5>Enter your student number to proceed with payment</h5>
        <form>
        <lable> Enter student number:
          <input type="text"/>
          <input type="submit"/>
        </lable>
    </form>
      </header>
    </div>
  );
}

export default App;

