import React, {useState, useEffect } from 'react';
import {
  Form,
  FormGroup,
  Input,
  Label
} from "reactstrap";
import '../styles.css';

const Home = () => {

  const [username, setUsername] = useState({
    username: '', });
  const [password, setPassword] = useState({
    password:'',});

  const [errors, setErrors] = useState(false);
  const [loading, setLoading] = useState(true);
  var [token, setToken] = useState('');

  useEffect(() => {
    if (token['token'] === 202) {
      window.location.replace('http://localhost:3000/history');
      
    } else {
    setLoading(false);
  }
  }, [token]);
 
  const onSubmit = e => {
    e.preventDefault();
    
    // Send request
    var axios = require('axios');
    var data = JSON.stringify({
      "username": username,
      "password": password
    });
    
    var config = {
      method: 'post',
      url: '/api/v1/login',
      headers: { 
        'Content-Type': 'application/json', 
        'Cookie': 'csrftoken=TxP6VZK6BgGSw3cwhiNtPssbf2C8IgeIHCGmUDpYGHR1VzGPEvv1OsEcqv9jd5n7; sessionid=af3asgeldjf9ov6o8801x184jjp3q4u2'
      },
      data : data
    };
    
    axios(config)
    .then(function (response) {
      setToken({ token: response.status})
      console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
      setErrors(true);
      console.log(error.response.status)
      console.log(error);
    });
  };
  
    return (
      <div className="Home">
        {loading === false && <h2 className='d-flex justify-content-center'>Login</h2>}
        {errors === true && <h2>Login Failed</h2>}
        {loading === false && (
        <Form className="form" onSubmit={onSubmit}>
          <FormGroup>
            <Label for="username">Username</Label>
            <Input
              autoFocus={true}
              type="username"
              name="username"
              value={username.username}
              required
              placeholder="username"
              onChange={e => setUsername(e.target.value)}
            />{' '}
            <br/>
            <Label for="password">Password</Label>
            <Input
              type="password"
              name="password"
              value={password.password}
              required
              placeholder="**********"
              onChange={e => setPassword(e.target.value)}
            />{' '}
          </FormGroup>
        <input type="submit" value='Login'></input>
      </Form>
        )}
    </div>
  );
};

export default Home;