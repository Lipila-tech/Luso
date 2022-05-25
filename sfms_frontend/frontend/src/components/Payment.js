import "react-table-6/react-table.css";
import "bootstrap/dist/css/bootstrap.min.css";
import React, {useEffect } from 'react';


const Account = () => {

  const [amount, setAmount] = React.useState({
    amount: '',
  });
  const [mobile, setMobile] = React.useState({
    mobile: ''
  });
  const [reference, setRef] = React.useState({
    reference: ''
  });
  const [errors, setErrors] = React.useState(false);
  const [paid, setPaid] = React.useState(false);

  const handleRefChange = event => {
    setRef({
      reference: event.target.value 
    });
  }

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
    useEffect(() => {
      if (paid['paid'] === 201) {
        setPaid(true);
      }
    }, [paid]);

  const handleSubmit = event => {
      event.preventDefault();

      var axios = require('axios');
      var data = JSON.stringify({
      "student": reference['reference'],
      "amount": amount['amount'],
      "mobile": mobile['mobile'],
      "reference": "12245",
      "pay_date": "2018-05-10",
      "term": "1"
      });

      var config = {
      method: 'post',
      url: '/api/v1/payments?id=2',
      headers: { 
          'Content-Type': 'application/json', 
          'X-CSFRToken': 's77416lj5sxno2icjzog90ips1b9xit8', 
          'Cookie': 'csrftoken=srORLevgm5wspjFS8eo4bMB48xQMU3biNZQ6hPp8LCOEgkL8Q2zp3kOHPRIjnzoa; sessionid=ayw57xsbo8httx6zpjf2pha5i4alq9pv'
      },
      data : data
      };

      axios(config)
      .then(function (response) {
        setPaid({paid: response.state})
      console.log(JSON.stringify(response.data));
      })
      .catch(function (error) {
      setErrors(true);
      console.log(error);
      });
    };

    return (
      <div className='container-lg'>
        {paid === true && <p className='d-flex justify-content-center'>Payment Sent Succesfully</p>}
        {errors === true && <p>Payment Failed</p>}
        <h2 className='d-flex justify-content-center'>Pay for Tuition</h2>
        <br/>
        {/* <SelectTableComponent /> */}
        <br/>
        <h2 className='d-flex justify-content-center'>Enter Amount and Account Number</h2>
        <br/>
        {/* <img src ={logo} alt='MTN Logo'/> */}
        <form onSubmit={handleSubmit}>
        <label>
            Student ID: {' '}
            <input autoFocus={true} type="text" value={reference.reference} onChange={handleRefChange} />
          </label>{" "}
        <label>
            Amount: {' '}
            <input autoFocus={true} type="text" value={amount.amount} onChange={handleAmountChange} />
          </label>{" "}
          <label>
            Mobile Number: {' '}
            <input autoFocus={true} type="text" placeholder='0963355664' value={mobile.mobile} onChange={handleMobileChange} />
          </label>{" "}
          <button type="submit">Submit</button>
        </form>
      </div>
    )
  }

export default Account