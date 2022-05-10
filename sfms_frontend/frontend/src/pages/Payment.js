import React, { Component } from 'react';  
import ReactTable from "react-table-6";  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import { Link } from "react-router-dom";
  
class Payment extends Component {  
  render() {  
     const data = [{  
        installment: 1,  
        pending: 3000,
        term: "term 1 2022",
        amount: 3000  
        },{  
         installment: 2,  
         pending: 2000,
         term: "term 1 2022",
         amount: 2400
         },
         {  
         installment: 3,  
         pending: 2000,
         term: "term 1 2022",
         amount: 2400
            }]  
     const columns = [{  
       Header: 'Installment',  
       accessor: 'installment'  
       },{  
       Header: 'Pending',  
       accessor: 'pending'  
       },
       {
         Header: 'Term',
         accessor: 'term'
       },
      {
        Header: "Amount to pay",
        accessor: "amount"
      }]  
    return (  
          <div className='container-lg'>  
            <h2 className='d-flex justify-content-center'>Make Payment</h2>
              <ReactTable  
              
                  data={data}  
                  columns={columns}  
                  defaultPageSize = {3}  
                  pageSizeOptions = {[2,4, 6]}  
              />
                <p className='d-flex justify-content-center'>Enter Total amount to pay: <input type="number" placeholder='amount'></input> Enter Mobile number to use: <input type="number" placeholder='0969620939'></input></p> 
                <Link className='d-flex justify-content-center' to={'/confirmation'}><button type="button" class="btn btn-primary">Proceed</button></Link>
          </div>        
    )  
  }  
}  
export default Payment;