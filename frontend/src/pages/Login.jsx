import React, { useState } from 'react';
import { Mail, Lock, ArrowRight, Loader2 } from 'lucide-react';

const Login = ({ onLogin, onBackToLanding }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      onLogin({ email });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-pulse-dark flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-pulse-card rounded-3xl border border-gray-800 p-10 shadow-2xl">
        <header className="text-center mb-10 space-y-2">
          <h2 className="text-3xl font-black text-white tracking-tight">Welcome Back</h2>
          <p className="text-gray-400">Log in to your Pulse AI dashboard.</p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
              <input 
                type="email" 
                required
                placeholder="Email Address" 
                className="w-full bg-pulse-dark border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-white focus:border-pulse-gold outline-none transition-colors"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
              <input 
                type="password" 
                required
                placeholder="Password" 
                className="w-full bg-pulse-dark border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-white focus:border-pulse-gold outline-none transition-colors"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-pulse-gold text-pulse-dark font-black py-4 rounded-xl shadow-lg hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center space-x-2"
          >
            {loading ? <Loader2 className="animate-spin" /> : (
              <>
                <span>Login to Dashboard</span>
                <ArrowRight size={20} />
              </>
            )}
          </button>
        </form>

        <div className="mt-8 text-center">
          <button onClick={onBackToLanding} className="text-sm text-gray-500 hover:text-pulse-gold transition-colors">
            Back to Landing Page
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
