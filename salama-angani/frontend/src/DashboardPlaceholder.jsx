import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from './api';

export default function DashboardPlaceholder() {
  const [flights, setFlights] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/api/flights')
      .then(res => setFlights(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    navigate('/login');
  };

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Flight Dashboard</h1>
        <button onClick={handleLogout} className="text-red-500 hover:underline">Logout</button>
      </div>
      <pre className="bg-gray-100 p-4 rounded-lg">{JSON.stringify(flights, null, 2)}</pre>
    </div>
  );
}