import React, { Component } from 'react';  
import ReactTable from "react-table-6";  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
  
class App extends Component { 
  state = {
        payments: [],
        pending: 3000
      }

componentDidMount() {
      axios.get(`api/v1/payments/`)
        .then(res => {
          const payments = res.data;
          this.setState({ payments });
          console.log(payments);
        })
    }

  render() {  
     const columns = [{  
       Header: 'Term',  
       accessor: 'term'  
       },{  
       Header: 'Date',  
       accessor: 'pay_date'  
       },
       {
         Header: 'Amount Paid',
         accessor: 'amount'
       },
     ]  
    return (  
          <div className='container-md'>  
            <h2 className='d-flex justify-content-center'>Payment History</h2>
            <br/>
              <ReactTable  
                  data={this.state.payments}
                  columns={columns}  
                  defaultPageSize = {3}  
                  pageSizeOptions = {[2,4, 6]}  
              />{' '}
              <br/>
               <a href={'/payments'} className="btn btn-primary d-flex justify-content-center">Make a Payment</a>
          </div>        
    )  
  }  
}  
export default App;