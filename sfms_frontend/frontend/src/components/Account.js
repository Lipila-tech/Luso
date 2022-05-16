import React from 'react';  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from 'axios';

export default class Account extends React.Component {
  state = {
    mobile: ''
  }

  handleChange = event => {
    this.setState({ mobile: event.target.value });
  }

  handleSubmit = event => {
    event.preventDefault();

    const user = {
      mobile: this.state.mobile
    };
    console.log(user.mobile)

    // axios.post(`api/v1/payments/`, { user })
    //   .then(res => {
    //     console.log(res);
    //     console.log(res.data);
    //   })
  }

  render() {
    return (
      <div className='container-lg'>
        <h2 className='d-flex justify-content-center'>Enter Account Number</h2>
        <br/>
        <img url='../assets/mtn.png' alt='MTN Logo'></img>
        <form onSubmit={this.handleSubmit}>
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
