import React from 'react';  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import SelectTableComponent from "./selectTableComponent";
  
export default function App() {  
  
    return (  
          <div className='container-lg'>  
            <h2 className='d-flex justify-content-center'>Select Items to Pay for</h2>
              <SelectTableComponent />
                <p >Enter Total amount to pay: <input type="number" placeholder='amount'></input></p> 
                <p >Enter Mobile number to use: <input type="number" placeholder='0969620939'></input></p>
                <a href={'/confirmation'} className="btn btn-primary d-flex justify-content-center">Proceed</a>
          </div>        
    );
  }  