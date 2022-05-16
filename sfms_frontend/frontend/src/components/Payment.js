import React from 'react';  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import SelectTableComponent from "./selectTableComponent";
import axios from 'axios';

export default class Payment extends React.Component {
  state = {
    amount: ''
  }

  handleChange = event => {
    this.setState({ amount: event.target.value });
  }

  handleSubmit = event => {
    event.preventDefault();

    const user = {
      amount: this.state.amount
    };
    console.log(user.amount)

    // axios.post(`api/v1/payments/`, { user })
    //   .then(res => {
    //     console.log(res);
    //     console.log(res.data);
    //   })
  }

  render() {
    return (
      <div className='container-lg'>
        <h2 className='d-flex justify-content-center'>Select Items to Pay for</h2>
        <br/>
        <SelectTableComponent />
        <br/>
        
        <form onSubmit={this.handleSubmit}>
          <label>
            Amount:{' '}
            <input type="number" name="amount" placeholder='1000' onChange={this.handleChange} />
          </label>{" "}
          <button type="submit">Next</button>
        </form>
      </div>
    )
  }
}
