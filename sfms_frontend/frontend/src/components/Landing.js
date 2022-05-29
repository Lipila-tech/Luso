import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import '../styles.css';
// Import medial
import banner from "../assets/banner2.jpg";
import PayGif from "../assets/payment.gif";
import AdmGif from "../assets/admin.gif";
import HisImg from "../assets/history.jpg";


const Landing = () => {

    return (
      <div>
        <div className="container">
         <div className="jumbotron text-center">
              <h2>A Student Fees Mangement System</h2>
              <h5>Allows Schools collect Tuition Fees online</h5>
              <h5>Students and Parents Pay using Mobile Money</h5>    
          </div>
          <div>
                <img className="embed-responsive-item" src={banner} alt="banner"/> 
          </div>
          <h3>Benefits</h3>
          <div className="row">
                    <div className="col-sm-4">
                        <ul>
                          <li>Saves Time</li>
                          <li>More Efficient</li>
                          <li>Secure and Reliable</li>
                          <li>Low Risk of Theft</li>
                          <li>Eliminate Carbon Footprint</li>
                        </ul>
                    </div>
                    <div className="col-sm-4"></div>
                    <div className="col-sm-4">
                        <ul>
                          <li>Reduces Labour</li>
                          <li>Quick and Easy Setup</li>
                          <li>Decreases Late Payments</li>
                          <li>Immediate Confirmation</li>
                          <li>Convenient Storage of Data</li>
                        </ul>
                    </div>
              </div>
        </div>
          <div className="container">
              <div className="jumbotron text-center">
                <h1 id="features">FEATURES</h1>
                <h3> Student payments</h3>
                <p>Students Can Make payments using MTN mobile money</p>
                <img src={PayGif} alt="student payment gif"/>
                <br/>
                <br/>
                <br/>
                <h3> Admin add Payment</h3>
                <p>Site administrators can also add payments via the backend</p>
                <img src={AdmGif} alt="admin payment gif"/>
                <br/>
                <br/>
                <br/>
                <h3> Student History</h3>
                <p>Students can view a history of their transactions</p>
                <img src={HisImg} alt="student history"/>
              </div>
          </div>
          
          <div className="container">
            <div className="jumbotron text-center">
              <h2 id="about">About The Project</h2>
              <p>This is a portfolio project for <a target="blank" href="https://www.holbertonschool.com/">Holberton School</a></p>
              <p>The project was inspired by the need to deconjest banks during back to school periods,</p>
              <p>reduce manaul labour for schools and save time and risk of money loss and thefts by students</p>
              <br/>
              <br/>
              <h4 id="bio"> Developer Bio</h4>
              My name is Peter Sangwani Zyambo and I am a full-stack Web Application Developer and Software Engineer, currently living in Kitwe, Copperbelt, Zambia. 
              My primary focus and inspiration for my studies is Web Development. In my free time, I study human computer interface and the psychology of human computer interaction.
              I am both driven and self-motivated, and I am constantly experimenting with new technologies and techniques. I am very passionate about software development,
              and strive to better myself as a developer, and the African development community as a whole mostly here in my country Zambia.
              <br/>
              <br/>
              <h4> Languages</h4>
              I develop in C, C++, Python and Java though I primarily use Python. I develop both the back and front-end, 
              and I am proficient in HTML/HTML5, CSS, JavaScript, React, jQuery and SQL/MySQL/PostgreSQL, to name a few. 
              I have worked on desktop, web and mobile applications.
              <br/>
              <br/>
              <div className="row" id="contact">
                    <div className="col-sm-4">
                        LinkedIn
                    </div>
                    <div className="col-sm-4">
                        Twitter
                    </div>
                    <div className="col-sm-4">
                       Github
                    </div>
              </div>
              <br/>
              <br/>
              <h4> Project Repo</h4>
              <br/>
                Github
             
            </div>
          </div>
    </div>
  );
};

export default Landing;