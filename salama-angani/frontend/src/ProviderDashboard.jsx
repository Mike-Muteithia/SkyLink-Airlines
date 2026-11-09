import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plane, LogOut, Plus, Loader2 } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import api from './api';

export default function ProviderDashboard() {
  const [formData, setFormData] = useState({
    flight_number: '', origin: '', destination: '', available_seats: '', base_price: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    toast.loading("Publishing flight...", { id: "publish" });

    try {
      await api.post('/api/flights', {
        ...formData,
        available_seats: parseInt(formData.available_seats),
        base_price: parseFloat(formData.base_price)
      });
      toast.success("Flight added to live inventory!", { id: "publish" });
      setFormData({ flight_number: '', origin: '', destination: '', available_seats: '', base_price: '' });
    } catch (err) {
      toast.error(err.response?.data?.error || "Failed to publish flight", { id: "publish" });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Toaster position="bottom-right" />
      <nav className="bg-white shadow-sm border-b border-gray-100 px-8 py-4 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-2 text-primary">
          <Plane className="w-6 h-6" />
          <span className="text-xl font-bold text-gray-900">Salama Provider Admin</span>
        </div>
        <button onClick={handleLogout} className="flex items-center gap-2 text-gray-500 hover:text-red-500 transition-colors">
          <LogOut className="w-5 h-5" />
          <span className="text-sm font-medium">Logout</span>
        </button>
      </nav>

      <main className="max-w-2xl mx-auto px-6 py-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Flight</h2>
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Origin</label>
                <input type="text" required value={formData.origin} onChange={e => setFormData({...formData, origin: e.target.value})} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none" placeholder="e.g. Nairobi" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
                <input type="text" required value={formData.destination} onChange={e => setFormData({...formData, destination: e.target.value})} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none" placeholder="e.g. Dubai" />
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Flight Number</label>
                <input type="text" required value={formData.flight_number} onChange={e => setFormData({...formData, flight_number: e.target.value})} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none uppercase" placeholder="SA-300" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Total Seats</label>
                <input type="number" required min="1" value={formData.available_seats} onChange={e => setFormData({...formData, available_seats: e.target.value})} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none" placeholder="150" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Base Price ($)</label>
                <input type="number" required min="1" step="0.01" value={formData.base_price} onChange={e => setFormData({...formData, base_price: e.target.value})} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none" placeholder="299.99" />
              </div>
            </div>
            <button type="submit" disabled={isSubmitting} className="w-full py-3 mt-4 bg-primary hover:bg-purple-700 text-white rounded-xl font-semibold flex justify-center items-center gap-2 transition-colors">
              {isSubmitting ? <Loader2 className="w-5 h-5 animate-spin" /> : <Plus className="w-5 h-5" />}
              Publish Flight
            </button>
          </form>
        </motion.div>
      </main>
    </div>
  );
}