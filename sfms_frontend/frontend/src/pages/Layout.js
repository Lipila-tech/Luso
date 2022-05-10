import { Outlet, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

const Layout = () => {
  return (
      <>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
<h1 class="nav-link active" aria-current="page" >Student Fees Management</h1>
<div>
  <ul class="nav justify-content-end">
    <li class="nav-item active">
      <Link class="nav-link" to={'#'} >Welcome,<span class="sr-only">USER.</span></Link>
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
  </ul>
</div>
</nav>
<Outlet/>
</>
  )
};

export default Layout;