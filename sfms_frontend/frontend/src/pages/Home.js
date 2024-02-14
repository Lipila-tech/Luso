import { Component } from 'react';
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
<<<<<<< HEAD
        <h2>Sign In</h2>
=======
        <h2 className='d-flex justify-content-center'>Enter Code to Make a Payment</h2>
>>>>>>> e5e2db4 (update frontend)
        <Form className="form">
          <FormGroup>
            <Label for="exampleEmail">Username</Label>
            <Input
              type="email"
              name="email"
              id="exampleEmail"
              placeholder="example@example.com"
            />
          </FormGroup>
          <FormGroup>
            <Label for="examplePassword">Password</Label>
            <Input
              type="password"
              name="password"
              id="examplePassword"
              placeholder="********"
            />
          </FormGroup>
        <Button>Submit</Button>
      </Form>
    </div>
  );
}
}

export default Home;