import { Component } from 'react';  
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
    <ul class="card-title">
      <li>User. You are Paying a sum of ZMW{this.props.amount}</li>
      <li>Using Mobile account#: {this.props.mobile}</li>
      <li>A prompt will be sent to your number for confirmation</li>
    </ul>
    <br/>
    <a href={'/'} class="btn btn-primary">Confirm</a>
  </div>
</div>
            <div className='d-flex justify-content-center'>
                <a href={'/payment'} class="btn btn-primary">Go back</a>
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