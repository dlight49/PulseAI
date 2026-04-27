import React, { useState } from 'react';
import { CreditCard, Lock, AlertCircle, Loader2, CheckCircle } from 'lucide-react';

const TrialExpired = ({ onPaymentSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handlePayment = () => {
    setLoading(true);
    // Simulate Payment Gateway (Paystack/Flutterwave)
    setTimeout(() => {
      setSuccess(true);
      setLoading(false);
      setTimeout(() => {
        onPaymentSuccess();
      }, 2000);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-pulse-dark flex items-center justify-center p-6 text-pulse-text">
      <div className="max-w-lg w-full bg-pulse-card rounded-[2rem] border-2 border-pulse-gold/30 p-12 shadow-[0_0_50px_rgba(241,196,15,0.1)] relative overflow-hidden">
        
        {!success ? (
          <div className="space-y-8 text-center animate-in fade-in zoom-in duration-500">
            <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <Lock className="text-red-500" size={40} />
            </div>
            
            <header className="space-y-4">
              <h2 className="text-4xl font-black tracking-tight text-white">Trial Period Expired</h2>
              <p className="text-gray-400 text-lg leading-relaxed">
                Your 7-day executive trial has concluded. To continue using Pulse AI to grow your business, please upgrade to a professional plan.
              </p>
            </header>

            <div className="bg-pulse-dark/50 border border-gray-800 rounded-2xl p-6 text-left space-y-4">
              <div className="flex items-start space-x-4">
                <AlertCircle className="text-pulse-gold shrink-0" size={20} />
                <p className="text-sm text-gray-300 italic">
                  "Your WhatsApp AI will remain inactive until payment is confirmed."
                </p>
              </div>
              <div className="pt-4 border-t border-gray-800 flex justify-between items-center">
                <span className="text-gray-400">Professional Plan</span>
                <span className="text-2xl font-bold text-pulse-gold">₦25,000<span className="text-sm font-normal text-gray-500">/mo</span></span>
              </div>
            </div>

            <button 
              onClick={handlePayment}
              disabled={loading}
              className="w-full bg-pulse-gold text-pulse-dark font-black py-5 rounded-2xl shadow-xl hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center space-x-3 text-lg"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" />
                  <span>Processing Secure Payment...</span>
                </>
              ) : (
                <>
                  <CreditCard size={24} />
                  <span>UPGRADE NOW</span>
                </>
              )}
            </button>
            
            <p className="text-xs text-gray-500 uppercase tracking-widest font-bold">Secure checkout via Paystack</p>
          </div>
        ) : (
          <div className="text-center space-y-6 animate-in zoom-in duration-500 py-10">
            <div className="w-24 h-24 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-6 border border-green-500/30">
              <CheckCircle className="text-green-500" size={48} />
            </div>
            <h2 className="text-4xl font-black text-white">Payment Confirmed!</h2>
            <p className="text-gray-400 text-lg">Your account has been reactivated. Redirecting to your dashboard...</p>
          </div>
        )}

      </div>
    </div>
  );
};

export default TrialExpired;
