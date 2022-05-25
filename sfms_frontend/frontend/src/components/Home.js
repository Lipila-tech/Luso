import React, {useState, useEffect } from 'react';
import {
  Form,
  FormGroup,
  Input,
  Label
} from "reactstrap";
import '../styles.css';

const Home = () => {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      window.location.replace('http://localhost:3000/dashboard');
    } else {
      setLoading(false);
    }
  }, []);

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
          'Content-Type': 'application/json'
        },
        data : data
      };

      axios(config)
      .then(function (response) {
        console.log(JSON.stringify(response.data));
      })
      .catch(function (error) {
        console.log(error);
      });

    // end request

    // fetch('http://127.0.0.1:8000/api/v1/users/auth/login/', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json'
    //   },
    //   body: JSON.stringify(user)
    // })
    //   .then(res => res.json())
    //   .then(data => {
    //     if (data.key) {
    //       localStorage.clear();
    //       localStorage.setItem('token', data.key);
    //       window.location.replace('http://localhost:3000/history');
    //     } else {
    //       setUsername('');
    //       setPassword('');
    //       localStorage.clear();
    //       setErrors(true);
    //     }
    //   });
  };
  
    return (
      <div className="Home">
        {loading === false && <h2 className='d-flex justify-content-center'>Login</h2>}
        {errors === true && <h2>Cannot log in with provided credentials</h2>}
        {loading === false && (
        <Form className="form" onSubmit={onSubmit}>
          <FormGroup>
            <Label for="username">Username</Label>
            <Input
              type="username"
              name="username"
              value={username}
              required
              placeholder="username"
              onChange={e => setUsername(e.target.value)}
            />{' '}
            <br/>
            <Label for="password">Password</Label>
            <Input
              type="password"
              name="password"
              value={password}
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