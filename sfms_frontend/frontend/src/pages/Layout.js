import { Outlet, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import React, {useState, useEffect, Fragment} from "react";

const Layout = () => {

  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      setIsAuth(true);
    }
  }, []);

  return (
      <>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
<h1 class="nav-link active" aria-current="page" >Student Fees Management</h1>
<div>
  <ul class="nav justify-content-end">
<<<<<<< HEAD
    <li class="nav-item active">
      <Link class="nav-link" to={'#'} >Welcome, USER<span class="sr-only">USER.</span></Link>
=======
    {isAuth === true ? (
      <Fragment>
        {' '}
        <li class="nav-item active">
      <Link class="nav-link" to={'#'} >Welcome, USER.</Link>
>>>>>>> b017735 (add auth features)
    </li>
    <li class="nav-item">
      <Link  class="nav-link" to="/payment">PAY /</Link>
    </li>
    <li class="nav-item">
      <Link  class="nav-link" to="/history">HISTORY /</Link>
    </li>
    <li class="nav-item">
      <Link class="nav-link" to="/">LOG OUT</Link>
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