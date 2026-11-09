import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plane, LogOut, Ticket, Download } from 'lucide-react';
import { Toaster } from 'react-hot-toast';
import api from './api';
import CheckoutModal from './CheckoutModal';

export default function Dashboard() {
  const [flights, setFlights] = useState([]);
  const [myBookings, setMyBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const userRole = localStorage.getItem('user_role');

  const fetchDashboardData = () => {
    Promise.all([
      api.get('/api/flights'),
      api.get('/api/bookings')
    ])
    .then(([flightsRes, bookingsRes]) => {
      setFlights(flightsRes.data);
      setMyBookings(bookingsRes.data);
      setLoading(false);
    })
    .catch(err => {
      console.error("Fetch error:", err);
      setLoading(false);
    });
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const openCheckout = (flight) => {
    setSelectedFlight(flight);
    setIsModalOpen(true);
  };

  const downloadPDF = async (pnr) => {
    try {
      const res = await api.get(`/api/bookings/${pnr}/ticket`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Ticket_${pnr}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("Failed to download ticket", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Toaster position="bottom-right" />
      <CheckoutModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} flight={selectedFlight} onBookingSuccess={fetchDashboardData} />

      <nav className="bg-white shadow-sm border-b border-gray-100 px-8 py-4 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-2 text-primary">
          <Plane className="w-6 h-6" />
          <span className="text-xl font-bold text-gray-900">Salama Angani</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium bg-purple-100 text-purple-700 px-3 py-1 rounded-full uppercase tracking-wider">{userRole}</span>
          <button onClick={handleLogout} className="flex items-center gap-2 text-gray-500 hover:text-red-500 transition-colors">
            <LogOut className="w-5 h-5" />
            <span className="text-sm font-medium">Logout</span>
          </button>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-12">
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-4">Where to next?</h1>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
            <div className="bg-gray-200 h-40 rounded-2xl"></div>
            <div className="bg-gray-200 h-40 rounded-2xl"></div>
          </div>
        ) : (
          <>
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
              {flights.map(flight => (
                <motion.div key={flight.id} whileHover={{ y: -4 }} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
                  <div className="flex justify-between items-start mb-6">
                    <div>
                      <p className="text-sm font-semibold text-gray-400 mb-1">{flight.flight_number}</p>
                      <h3 className="text-xl font-bold text-gray-900">{flight.origin} → {flight.destination}</h3>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-black text-primary">${flight.base_price.toFixed(2)}</p>
                      <p className="text-sm text-gray-500 font-medium">{flight.available_seats} seats left</p>
                    </div>
                  </div>
                  <button disabled={flight.available_seats <= 0} onClick={() => openCheckout(flight)} className="w-full py-3 px-4 bg-gray-900 hover:bg-gray-800 disabled:bg-gray-200 disabled:text-gray-400 text-white rounded-xl font-semibold flex justify-center items-center gap-2 transition-colors">
                    <Ticket className="w-5 h-5" />
                    {flight.available_seats > 0 ? 'Book Ticket' : 'Sold Out'}
                  </button>
                </motion.div>
              ))}
            </motion.div>

            {myBookings.length > 0 && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">My Tickets</h2>
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                  {myBookings.map((b, index) => (
                    <div key={b.pnr} className={`p-4 flex justify-between items-center ${index !== myBookings.length - 1 ? 'border-b border-gray-100' : ''}`}>
                      <div>
                        <p className="font-bold text-gray-900">{b.origin} → {b.destination} <span className="text-gray-400 font-normal ml-2">{b.flight_number}</span></p>
                        <p className="text-sm text-gray-500">Passenger: {b.passenger_name} • PNR: <span className="font-mono text-primary">{b.pnr}</span></p>
                      </div>
                      <button onClick={() => downloadPDF(b.pnr)} className="p-2 text-gray-500 hover:text-primary hover:bg-purple-50 rounded-lg transition-colors">
                        <Download className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </>
        )}
      </main>
    </div>
  );
}