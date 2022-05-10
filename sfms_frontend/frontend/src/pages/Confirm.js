import { Component } from 'react';  
import { Link } from "react-router-dom";


class Confirm  extends Component {
  render(){
    return (
        <div className="container">
            <h1 className='d-flex justify-content-center'>Confirm Payment</h1>
            <div class="card text-center">
  <div class="card-header">
    Pay with MoMo
  </div>
  <div class="card-body">
    <h5 class="card-title">User. You are Paying a sum of ZMW{this.props.amount} Using Mobile account#: {this.props.mobile}</h5>
    <h5 class="card-title"> A prompt will be sent to your number for confirmation</h5>
    <a href={'/'} class="btn btn-primary">Confirm</a>
  </div>
</div>
            <div className='d-flex justify-content-center'>
                <Link to={'/payment'}><button type="button" class="btn btn-primary"> Go Back </button></Link>
            </div>
        </div>
    )
  };
}

Confirm.defaultProps = {
  amount: 23455,
  mobile: "098765432"
}
export default Confirm;