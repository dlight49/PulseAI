import React from 'react';
import { 
  LayoutDashboard, 
  Brain, 
  MessageSquare, 
  History, 
  UserCheck, 
  Settings,
  LogOut
} from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'dashboard', label: 'ROI Command Center', icon: LayoutDashboard },
    { id: 'brain', label: 'Brain Configurator', icon: Brain },
    { id: 'conversations', label: 'Conversation Vault', icon: MessageSquare },
    { id: 'ledger', label: 'Transaction Ledger', icon: History },
    { id: 'destiny', label: 'Destiny Proxy', icon: UserCheck },
  ];

  return (
    <div className="h-screen w-64 bg-pulse-dark border-r border-gray-800 flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-pulse-gold tracking-tighter">PULSE AI</h1>
        <p className="text-xs text-gray-500 font-medium">EXECUTIVE PORTAL</p>
      </div>

      <nav className="flex-1 px-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
              activeTab === item.id 
                ? 'bg-pulse-gold text-pulse-dark font-bold shadow-lg' 
                : 'text-gray-400 hover:bg-pulse-card hover:text-white'
            }`}
          >
            <item.icon size={20} />
            <span className="text-sm">{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <button className="w-full flex items-center space-x-3 px-4 py-3 text-gray-400 hover:text-red-400 transition-colors">
          <LogOut size={20} />
          <span className="text-sm font-medium">Sign Out</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
