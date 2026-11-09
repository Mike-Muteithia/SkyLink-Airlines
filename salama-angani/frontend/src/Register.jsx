import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import api from './api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // We explicitly set the role to 'customer'
      await api.post('/api/auth/register', { email, password, role: 'customer' });
      toast.success("Account created successfully! Please log in.");
      navigate('/login');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Registration failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Toaster position="bottom-right" />
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white p-8 rounded-xl shadow-lg border border-gray-100"
      >
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-2">Create Account</h2>
        <p className="text-center text-gray-500 mb-8">Join Salama Angani to book your flights</p>
        
        <form onSubmit={handleRegister} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input 
              type="email" required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors"
              value={email} onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input 
              type="password" required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-colors"
              value={password} onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button 
            type="submit" disabled={isSubmitting}
            className="w-full bg-primary hover:bg-purple-700 text-white font-semibold py-2.5 rounded-lg transition-colors shadow-sm flex justify-center items-center gap-2"
          >
            {isSubmitting ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Sign Up'}
          </button>
        </form>
        
        <div className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-primary hover:underline font-semibold">
            Log in here
          </Link>
        </div>
      </motion.div>
    </div>
  );
}