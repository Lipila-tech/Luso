import React, { Component } from 'react';  
import ReactTable from "react-table-6";  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
  
class App extends Component {  
  render() {  
     const data = [{  
        date: '2022-05-05',  
        amount: 2645,
        term: "term 1 2022",
        pending: 3000  
        },{  
         date: '2022-10-10',  
         amount: 2345,
         term: "term 2 2022",
         pending: 2400
         }];
     const columns = [{  
       Header: 'Transaction date',  
       accessor: 'date'  
       },{  
       Header: 'Amount',  
       accessor: 'amount'  
       },
       {
         Header: 'Term',
         accessor: 'term'
       },
      {
        Header: "Pending",
        accessor: "pending"
      }]  
    return (  
          <div className='container-lg'>  
            <h2 className='d-flex justify-content-center'>Payment History</h2>
              <ReactTable  
                  data={data}  
                  columns={columns}  
                  defaultPageSize = {3}  
                  pageSizeOptions = {[2,4, 6]}  
              />
               <a href={'/payment'} class="btn btn-primary d-flex justify-content-center">Make a Payment</a>
          </div>        
    )  
  }  
}  
export default App;