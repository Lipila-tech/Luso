import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import '../styles.css';
// Import medial
import banner from "../assets/banner1.jpg"
import PayGif from "../assets/payment.gif"
import AdmGif from "../assets/admin.gif"
import HisImg from "../assets/history.png"

const Landing = () => {

    return (
      <div>
        <section>
          <h2>A Student Fees Mangement System</h2>
          <h2>That allows you to collect Tuition Fees online</h2>
          <h2>Student's Pay using MTN Mobile Money</h2>
          <img src={banner} alt="banner"/>
        </section>

        <section>
          <h1>FEATURES</h1>
          <h3> Student payments</h3>
          <p>Students Can Make payments using MTN mobile money</p>
          <img src={PayGif} alt="student payment gif"/>
          <h3> Admin add Payment</h3>
          <p>Site administrators can also add payments via the backend</p>
          <img src={AdmGif} alt="admin payment gif"/>
          <h3> Student History</h3>
          <p>Students can view a history of their transactions</p>
          <img src={HisImg} alt="student history"/>
          
        </section>

        <section>
          <h1>ABOUT</h1>
          <p>This is a portfolio project for <a target="blank" href="https://www.holbertonschool.com/">Holberton School</a></p>
          The project was inspired by the need to deconjest banks during back to school periods,
          reduce manaul work for school finance departments, and improve peoples productivity overall.

          <h4>Developer: Peter Sangwani Zyambo</h4>
          <a href="#">LinkedIn</a> 
          <a href="#">Twitter</a> 
          <a href="#">Github</a> 

          <h3>Project Repository</h3>
          <a href="#">Github</a> 
        </section>
    </div>
  );
};

export default Landing;