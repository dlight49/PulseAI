import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import BrainConfig from './pages/BrainConfig';
import ConversationVault from './pages/ConversationVault';
import TransactionLedger from './pages/TransactionLedger';
import DestinyMode from './pages/DestinyMode';
import Onboarding from './pages/Onboarding';
import { Menu, X } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isOnboarded, setIsOnboarded] = useState(false); // New user state

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

  if (!isOnboarded) {
    return <Onboarding onComplete={() => setIsOnboarded(true)} />;
  }

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
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
