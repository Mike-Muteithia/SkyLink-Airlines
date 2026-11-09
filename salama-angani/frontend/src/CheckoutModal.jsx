import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, CreditCard, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import api from './api';

// Luhn Algorithm for validating credit card numbers
const isValidLuhn = (value) => {
  const sanitized = value.replace(/\D/g, '');
  if (!sanitized) return false;
  let sum = 0;
  let shouldDouble = false;
  for (let i = sanitized.length - 1; i >= 0; i--) {
    let digit = parseInt(sanitized.charAt(i));
    if (shouldDouble) {
      if ((digit *= 2) > 9) digit -= 9;
    }
    sum += digit;
    shouldDouble = !shouldDouble;
  }
  return sum % 10 === 0;
};

export default function CheckoutModal({ isOpen, onClose, flight, onBookingSuccess }) {
  const [passengerName, setPassengerName] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleCheckout = async (e) => {
    e.preventDefault();
    
    if (!isValidLuhn(cardNumber)) {
      toast.error("Invalid credit card number.");
      return;
    }

    setIsProcessing(true);
    toast.loading("Processing payment...", { id: "payment" });

    try {
      // 1. Process Payment
      const res = await api.post('/api/bookings', {
        flight_id: flight.id,
        passenger_name: passengerName
      });
      toast.success(`Payment Approved! PNR: ${res.data.booking_reference}`, { id: "payment", duration: 5000 });
      onBookingSuccess();
      
      // 2. Download PDF Ticket
      try {
        const pdfRes = await api.get(`/api/bookings/${res.data.booking_reference}/ticket`, { responseType: 'blob' });
        // Create a hidden link to trigger the browser's download prompt
        const url = window.URL.createObjectURL(new Blob([pdfRes.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `Ticket_${res.data.booking_reference}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (pdfErr) {
        toast.error("Payment successful, but failed to download PDF.", { duration: 4000 });
      }

      onClose();
    } catch (err) {
      toast.error(err.response?.data?.error || "Transaction failed", { id: "payment" });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden"
          >
            <div className="flex justify-between items-center p-6 border-b border-gray-100 bg-gray-50">
              <h2 className="text-xl font-bold text-gray-900">Secure Checkout</h2>
              <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCheckout} className="p-6 space-y-6">
              <div className="bg-purple-50 p-4 rounded-xl border border-purple-100 flex justify-between items-center">
                <div>
                  <p className="text-sm text-purple-600 font-semibold mb-1">Total Amount</p>
                  <p className="text-2xl font-black text-gray-900">${flight.base_price.toFixed(2)}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-700">{flight.origin} → {flight.destination}</p>
                  <p className="text-xs text-gray-500">Flight {flight.flight_number}</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Passenger Full Name</label>
                <input 
                  type="text" required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none"
                  value={passengerName} onChange={e => setPassengerName(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Card Number</label>
                <div className="relative">
                  <CreditCard className="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
                  <input 
                    type="text" required maxLength="19" placeholder="0000 0000 0000 0000"
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none font-mono"
                    value={cardNumber} onChange={e => setCardNumber(e.target.value)}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Expiry Date</label>
                  <input type="text" required placeholder="MM/YY" className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">CVC</label>
                  <input type="text" required placeholder="123" maxLength="4" className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary outline-none" />
                </div>
              </div>

              <button 
                type="submit" disabled={isProcessing}
                className="w-full py-3 px-4 bg-gray-900 hover:bg-gray-800 disabled:bg-gray-400 text-white rounded-xl font-semibold flex justify-center items-center gap-2 transition-colors"
              >
                {isProcessing ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Confirm & Pay'}
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}