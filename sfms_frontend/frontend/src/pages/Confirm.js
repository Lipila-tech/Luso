import { Link } from "react-router-dom";

const Confirm = () => {
    return (
        <div className="container">
            <h1 className='d-flex justify-content-center'>Confirm Payment</h1>
            <div class="card text-center">
  <div class="card-header">
    Pay with MoMo
  </div>
  <div class="card-body">
    <h5 class="card-title">User. You are Paying a sum of k200 Using Mobile number 203948775</h5>
    <h5 class="card-title"> A prompt will be sent to your number</h5>
    <a href={'/'} class="btn btn-primary">Confirm</a>
  </div>
</div>
            <div className='d-flex justify-content-center'>
                <Link to={'/payment'}><button type="button" class="btn btn-primary"> Go Back </button></Link>
            </div>
        </div>
    )
  };
  
  export default Confirm;