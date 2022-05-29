import React, { Component } from 'react';  
import ReactTable from "react-table-6";  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import {
  Form,
  FormGroup,
  Input,
  Label
} from "reactstrap";
  
class App extends Component { 
  state = {
        payments: [],
        isAuth: true,
        id: '',
        errors: false
      }


      onSubmit = (e) =>{
        console.log(this.state.id)
        // this.setState({
        //   id: parseInt(this.state.id)})

        if (this.state.id === 3) {
          this.setState({isAuth: true})
        }
      }

      setUserId (e) {
        this.setState({id: e.target.value})
      }
componentDidMount() {
  console.log(this.state.id)

    axios.get("/api/v1/history?id=2")
      .then((res) => {
        const payments = res.data;
        var newPayments = this.state.payments.concat([payments]);
        this.setState({ payments: newPayments });
        console.log(JSON.stringify(res.data));
      })
        .catch((err) => console.log(err));
        this.setState({errors: true})
  } 

  render() {  
    
     const columns = [{  
      Header: 'Pay Date',  
      accessor: 'paydate'  
      },
       {  
       Header: 'Term',  
       accessor: 'term'  
       },
       {
         Header: 'Amount Paid',
         accessor: 'amount'
       },
       {
        Header: 'Pending',
        accessor: 'pending'
      },
      {
        Header: 'Account',
        accessor: 'account'
      },
      {
        Header: 'Reference',
        accessor: 'reference'
      },
     ]  
    return (  
          <div className='container-md'>  
            <h2 className='d-flex justify-content-center'>Payment History</h2>
            <br/>
            { this.state.isAuth === true && <div>
              <ReactTable  
                    data={this.state.payments}
                    columns={columns}  
                    defaultPageSize = {3}  
                    pageSizeOptions = {[2,4, 6]}  
                />{' '}
                <br/>
                <a href={'/payments'} className="btn btn-primary d-flex justify-content-center">Make a Payment</a>
               </div>}
               { this.state.isAuth === false && <div>
                 {this.state.errors === true && <p> Failed to get history check student number</p>}
                 <h3>Enter Student ID to Check History</h3>
                 <Form className="form" onSubmit={this.onSubmit}>
                    <FormGroup>
                      <Label for="username">Student ID</Label>
                      <Input
                        autoFocus={true}
                        type="text"
                        // value={this.state.id}
                        required
                        placeholder="student id"
                        onChange={this.setUserId}
                      />{' '}
                      <br/>
                    </FormGroup>
                  <input type="submit" value='Submit'></input>
                </Form>

               </div>}
          </div>        
    )  
  }  
}  
export default App;