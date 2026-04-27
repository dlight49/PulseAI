import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import BrainConfig from './pages/BrainConfig';
import ConversationVault from './pages/ConversationVault';
import TransactionLedger from './pages/TransactionLedger';
import DestinyMode from './pages/DestinyMode';
import Onboarding from './pages/Onboarding';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import TrialExpired from './pages/TrialExpired';
import { Menu, X } from 'lucide-react';

function App() {
  const [view, setView] = useState('landing'); // landing, signup, login, dashboard, expired
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [user, setUser] = useState(null);

  // Check trial status whenever user changes or view changes to dashboard
  useEffect(() => {
    if (user && view === 'dashboard') {
      const trialDays = 7;
      const signupDate = new Date(user.trialStartedAt || Date.now());
      const now = new Date();
      const diffTime = Math.abs(now - signupDate);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays > trialDays && !user.isPaid) {
        setView('expired');
      }
    }
  }, [user, view]);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'brain':
        return <BrainConfig />;
      case 'conversations':
        return <ConversationVault />;
      case 'ledger':
        return <TransactionLedger />;
      case 'destiny':
        return <DestinyMode />;
      default:
        return (
          <div className="p-8 flex items-center justify-center h-[80vh]">
            <p className="text-gray-600 font-bold tracking-widest uppercase">Feature in active development</p>
          </div>
        );
    }
  };

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
    setIsMobileMenuOpen(false); 
  };

  const startTrial = () => setView('signup');
  const openLogin = () => setView('login');
  
  const handleSignupComplete = (userData) => {
    setUser({
      ...userData,
      trialStartedAt: new Date().toISOString(),
      isPaid: false
    });
    setView('dashboard');
  };

  const handleLogin = (credentials) => {
    // For demo, we simulate a user who has already used their trial
    const mockUser = {
      email: credentials.email,
      business_name: 'Demo Business',
      trialStartedAt: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(), // 8 days ago
      isPaid: false
    };
    setUser(mockUser);
    setView('dashboard');
  };

  const handlePaymentSuccess = () => {
    setUser(prev => ({ ...prev, isPaid: true }));
    setView('dashboard');
  };

  if (view === 'landing') return <LandingPage onStartTrial={startTrial} onLogin={openLogin} />;
  if (view === 'signup') return <Onboarding onComplete={handleSignupComplete} />;
  if (view === 'login') return <Login onLogin={handleLogin} onBackToLanding={() => setView('landing')} />;
  if (view === 'expired') return <TrialExpired onPaymentSuccess={handlePaymentSuccess} />;

  return (
    <div className="flex bg-pulse-dark min-h-screen text-pulse-text font-sans">
      
      {/* MOBILE HEADER */}
      <div className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-pulse-dark border-b border-gray-800 flex items-center justify-between px-6 z-50">
        <h1 className="text-xl font-bold text-pulse-gold tracking-tighter">PULSE AI</h1>
        <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-gray-400 p-2">
          {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* DESKTOP SIDEBAR */}
      <div className="hidden lg:block">
        <Sidebar activeTab={activeTab} setActiveTab={handleTabChange} />
      </div>

      {/* MOBILE DRAWER */}
      {isMobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-40 bg-black bg-opacity-80 animate-in fade-in duration-300">
          <div className="w-64 h-full bg-pulse-dark animate-in slide-in-from-left duration-300">
             <Sidebar activeTab={activeTab} setActiveTab={handleTabChange} />
          </div>
        </div>
      )}
      
      {/* MAIN COMMAND AREA */}
      <main className="flex-1 overflow-y-auto mt-16 lg:mt-0 pb-10">
        <div className="p-4 lg:p-8 flex justify-between items-center border-b border-gray-800 mb-6 bg-pulse-dark/50 sticky top-0 z-30 backdrop-blur-md">
           <div>
              <h2 className="text-sm font-bold text-pulse-gold uppercase tracking-[0.2em]">Active Session</h2>
              <p className="text-2xl font-black text-white">{user?.business_name || 'Executive Dashboard'}</p>
           </div>
           {!user?.isPaid && (
             <div className="bg-pulse-gold/10 border border-pulse-gold/30 px-4 py-2 rounded-full">
               <span className="text-pulse-gold text-xs font-bold uppercase tracking-widest animate-pulse">Trial Mode Active</span>
             </div>
           )}
        </div>
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
