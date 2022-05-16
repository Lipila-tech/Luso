import React from 'react';  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import SelectTableComponent from "./selectTableComponent";
import axios from 'axios';

export default class Payment extends React.Component {
  state = {
    name: ''
  }

  handleChange = event => {
    this.setState({ name: event.target.value });
  }

  handleSubmit = event => {
    event.preventDefault();

    const user = {
      name: this.state.name
    };

    axios.post(`api/v1/payments/`, { user })
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
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
          <label>
            Mobile Number: {' '}
            <input type="text" name="mobile" placeholder='0969229988' onChange={this.handleChange} />
          </label>{" "}
          <button type="submit">Submit</button>
        </form>
      </div>
    )
  }
}