import React from 'react';  
import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import SelectTableComponent from './selectTableComponent';
import axios from 'axios';

const Account = () => {

  const [amount, setAmount] = React.useState({
    amount: ''
  });
  const [mobile, setMobile] = React.useState({
    mobile: ''
  });

  const handleAmountChange = event => {
    setAmount({
      amount: event.target.value 
    });
  }

  const handleMobileChange = event => {
    setMobile({
      mobile: event.target.value 
    });
  }

  const handleSubmit = event => {
    event.preventDefault();

    const data = {
      mobile: mobile.mobile,
      amount: amount.amount
    };
    console.log(data.mobile)
    console.log(data.amount)

    // axios.post(`api/v1/payments/`, { user })
    //   .then(res => {
    //     console.log(res);
    //     console.log(res.data);
    //   })
  }

    return (
      <div className='container-lg'>
        <h2 className='d-flex justify-content-center'>Select Items to Pay for</h2>
        <br/>
        <SelectTableComponent />
        <br/>
        <img src ='../assets/mtn.png' alt='MTN Logo'></img>
        <h2 className='d-flex justify-content-center'>Enter Amount and Account Number</h2>
        <br/>
        <form onSubmit={handleSubmit}>
        <label>
            Amount: {' '}
            <input autoFocus={true} type="text" value={amount.amount} onChange={handleAmountChange} />
          </label>{" "}
          <label>
            Mobile Number: {' '}
            <input autoFocus={true} type="text" placeholder='0969620939' value={mobile.mobile} onChange={handleMobileChange} />
          </label>{" "}
          <button type="submit">Submit</button>
        </form>
      </div>
    )
  }

export default Account