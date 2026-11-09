import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import ProviderDashboard from './ProviderDashboard';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('user_role');
  
  if (!token) return <Navigate to="/login" />;
  
  // Intercept the route for providers
  if (role === 'provider') return <ProviderDashboard />;
  
  return children;
};

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}