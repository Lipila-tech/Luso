import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Payment from "./components/Payment";
import History from "./components/History";
import Layout from "./components/Layout";
import Logout from "./components/Logout";
import Landing from "./components/Landing";


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
        <Route index element={<Landing />} /> 
          <Route path="history" element={<History />} />
          <Route path="payments" element={<Payment />} /> 
          <Route path="logout" element={<Logout />} /> 
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);