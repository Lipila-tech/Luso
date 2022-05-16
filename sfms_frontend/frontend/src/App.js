import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Home";
import Payment from "./pages/Payment";
import History from "./pages/History";
import Layout from "./pages/Layout";
import Confirm from "./pages/Confirm";

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