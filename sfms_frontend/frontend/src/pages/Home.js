import { Component } from 'react';
import { Link } from "react-router-dom";
import {
  Button,
  Form,
  FormGroup,
  Input,
  Label
} from 'reactstrap';
import '../styles.css';

class Home extends Component {
  render() {
    return (
      <div className="Home">
        <h2 className='d-flex justify-content-center'>Sign in to Make Payment</h2>
        <Form className="form">
          <FormGroup>
            <Label for="studentCode">Student Code</Label>
            <Input
              type="text"
              name="text"
              id="studentCode"
              placeholder="123456"
            />
          </FormGroup>
        <Link to={ '/history' }><Button>Submit</Button></Link>
      </Form>
    </div>
  );
}
}

export default Home;