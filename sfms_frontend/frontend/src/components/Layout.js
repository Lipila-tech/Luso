import { Outlet, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import React, {useState, useEffect, Fragment} from "react";
import logo from "../assets/d.png";

const Layout = () => {

  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    setIsAuth(true);
  }, []);

  return (
      <>
  <nav className="navbar navbar-expand-lg navbar-light bg-light">
  <a href="#" class="navbar-brand">
            <img src={logo} height="28" alt="logo"/>
    </a>
  <Link to={'/'} className="nav-link active"  aria-current="page" ><h1>SkoolPay</h1></Link>
{/* <h1 className="nav-link active" aria-current="page" >SkoolPay</h1> */}
<div className="container">
  <ul className="nav justify-content-end">
    {isAuth === true ? (
      <Fragment>
        {' '}
        <li className="nav-item active">
      <a className="nav-link" href="https://sfms-backend.herokuapp.com/admin" target="blank">Login</a>
    </li>
    <li className="nav-item">
      <Link  className="nav-link" to="/payments">PAY /</Link>
    </li>
    <li className="nav-item">
      <Link  className="nav-link" to="/history">HISTORY /</Link>
    </li>
    <li className="nav-item">
      <a className="nav-link" href="#features">FEATURES /</a>
    </li>
    <li className="nav-item">
      <a className="nav-link" href="#about">ABOUT /</a>
    </li>
    <li className="nav-item">
      <a className="nav-link" href="#bio">BIO</a>
    </li>
      </Fragment>
    ) : (
      <Fragment>
        {' '}
      </Fragment>
    )}
  </ul>
</div>
</nav>
<Outlet/>
</>
  )
};

export default Layout;