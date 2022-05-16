import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Home";
import Payment from "./components/Payment";
import History from "./components/History";
import Layout from "./components/Layout";
import Confirm from "./components/Confirm";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Login />} />
          <Route path="payments" element={<Payment />} />
          <Route path="history" element={<History />} />
          <Route path="confirmation" element={<Confirm />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);