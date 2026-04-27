import React, { useState } from 'react';
import { 
  Rocket, 
  CheckCircle, 
  ArrowRight, 
  MessageSquare,
  Building2,
  Mail
} from 'lucide-react';

const Onboarding = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    business_name: '',
    email: ''
  });

  const nextStep = () => {
    setLoading(true);
    setTimeout(() => {
      setStep(step + 1);
      setLoading(false);
    }, 1200);
  };

  return (
    <div className="min-h-screen bg-pulse-dark flex items-center justify-center p-6 animate-in fade-in duration-700">
      <div className="max-w-md w-full bg-pulse-card rounded-3xl border border-gray-800 p-8 shadow-2xl relative overflow-hidden">
        
        {/* Step Indicator */}
        <div className="flex space-x-2 mb-10">
          {[1, 2, 3].map((s) => (
            <div key={s} className={`h-1.5 flex-1 rounded-full transition-all duration-500 ${
              step >= s ? 'bg-pulse-gold shadow-[0_0_10px_rgba(241,196,15,0.4)]' : 'bg-gray-800'
            }`} />
          ))}
        </div>

        {/* STEP 1: IDENTITY */}
        {step === 1 && (
          <div className="space-y-6 animate-in slide-in-from-right duration-500">
            <header className="space-y-2">
              <h2 className="text-3xl font-bold text-white tracking-tight">Create your account</h2>
              <p className="text-gray-400 text-sm">Let's set up your executive profile.</p>
            </header>
            <div className="space-y-4 pt-4">
              <div className="relative">
                <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
                <input 
                  type="text" 
                  placeholder="Business Name" 
                  className="w-full bg-pulse-dark border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-white focus:border-pulse-gold outline-none"
                  value={formData.business_name}
                  onChange={(e) => setFormData({...formData, business_name: e.target.value})}
                />
              </div>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
                <input 
                  type="email" 
                  placeholder="Business Email" 
                  className="w-full bg-pulse-dark border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-white focus:border-pulse-gold outline-none"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                />
              </div>
              <button 
                onClick={nextStep}
                disabled={!formData.business_name || !formData.email || loading}
                className="w-full bg-pulse-gold text-pulse-dark font-black py-4 rounded-xl shadow-lg hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center space-x-2"
              >
                {loading ? <div className="w-5 h-5 border-2 border-pulse-dark border-t-transparent rounded-full animate-spin"></div> : (
                  <>
                    <span>Next Step</span>
                    <ArrowRight size={20} />
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: WHATSAPP HANDSHAKE */}
        {step === 2 && (
          <div className="space-y-6 animate-in slide-in-from-right duration-500">
            <header className="space-y-2">
              <h2 className="text-3xl font-bold text-white tracking-tight">Connect WhatsApp</h2>
              <p className="text-gray-400 text-sm">Pulse AI needs permission to handle your chats.</p>
            </header>
            <div className="py-8 flex flex-col items-center space-y-8">
              <div className="w-24 h-24 bg-[#25D366]/10 rounded-full flex items-center justify-center border border-[#25D366]/30">
                <MessageSquare size={48} fill="#25D366" className="text-[#25D366]" />
              </div>
              <ul className="text-sm text-gray-400 space-y-3 w-full">
                <li className="flex items-center space-x-3">
                  <CheckCircle size={16} className="text-green-400" />
                  <span>Secure Meta OAuth Handshake</span>
                </li>
                <li className="flex items-center space-x-3">
                  <CheckCircle size={16} className="text-green-400" />
                  <span>No password required</span>
                </li>
                <li className="flex items-center space-x-3">
                  <CheckCircle size={16} className="text-green-400" />
                  <span>Connects in under 30 seconds</span>
                </li>
              </ul>
            </div>
            <button 
              onClick={nextStep}
              className="w-full bg-[#25D366] text-white font-black py-4 rounded-xl shadow-[0_0_20px_rgba(37,211,102,0.3)] hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center space-x-2"
            >
              <span>CONTINUE WITH WHATSAPP</span>
            </button>
          </div>
        )}

        {/* STEP 3: SUCCESS */}
        {step === 3 && (
          <div className="space-y-6 animate-in zoom-in duration-500 text-center">
            <div className="w-20 h-20 bg-pulse-gold/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <Rocket className="text-pulse-gold" size={40} />
            </div>
            <h2 className="text-3xl font-bold text-white tracking-tight">AI Deployment Ready</h2>
            <p className="text-gray-400 text-sm px-4">
              Your digital workforce is connected. Let's program its DNA to start closing sales.
            </p>
            <button 
              onClick={() => onComplete(formData)}
              className="w-full bg-white text-pulse-dark font-black py-4 rounded-xl shadow-lg hover:scale-[1.02] active:scale-95 transition-all mt-8"
            >
              GO TO BRAIN ROOM
            </button>
          </div>
        )}

      </div>
    </div>
  );
};

export default Onboarding;
