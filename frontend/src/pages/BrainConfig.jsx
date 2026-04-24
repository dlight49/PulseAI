import React, { useState } from 'react';
import { 
  Save, 
  ShieldAlert, 
  Plus, 
  Trash2, 
  Info,
  DollarSign,
  MessageSquare,
  Settings,
  Smartphone,
  ExternalLink
} from 'lucide-react';

const BrainConfig = () => {
  const [activeSection, setActiveTab] = useState('identity');
  const [isConnected, setIsConnected] = useState(false);

  return (
    <div className="p-4 md:p-8 space-y-8 animate-in slide-in-from-right duration-500">
      
      {/* CONNECTION STATUS CARD */}
      <div className={`p-6 rounded-2xl border flex flex-col md:flex-row items-center justify-between gap-6 transition-all ${
        isConnected ? 'bg-green-500/5 border-green-500/20' : 'bg-pulse-gold/5 border-pulse-gold/20'
      }`}>
        <div className="flex items-center space-x-4">
          <div className={`p-4 rounded-full border ${isConnected ? 'bg-green-500/10 border-green-500/30' : 'bg-pulse-gold/10 border-pulse-gold/30'}`}>
            <Smartphone className={isConnected ? 'text-green-400' : 'text-pulse-gold'} size={32} />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white uppercase tracking-tight">AI Connection Status</h3>
            <p className="text-gray-400 text-sm">
              {isConnected ? 'Pulse AI is currently selling on your WhatsApp number.' : 'Connect your WhatsApp Business account to start selling.'}
            </p>
          </div>
        </div>
        {!isConnected ? (
          <button onClick={() => setIsConnected(true)} className="flex items-center space-x-3 bg-[#25D366] text-white font-black px-8 py-4 rounded-xl shadow-[0_0_20px_rgba(37,211,102,0.2)] hover:scale-105 transition-all w-full md:w-auto justify-center">
            <MessageSquare size={20} fill="white" />
            <span>CONNECT WHATSAPP NOW</span>
          </button>
        ) : (
          <div className="flex items-center space-x-2 text-green-400 font-bold px-6 py-2 bg-green-500/10 rounded-full border border-green-500/20">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span>LIVE & SELLING</span>
          </div>
        )}
      </div>

      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-white">Brain Configurator</h2>
          <p className="text-gray-400 text-sm md:text-base">Inject your company's DNA, rules, and pricing into the Pulse AI Brain.</p>
        </div>
        <button className="flex items-center justify-center space-x-2 bg-pulse-gold text-pulse-dark font-bold px-6 py-3 rounded-lg shadow-lg hover:brightness-110 transition-all w-full md:w-auto">
          <Save size={20} />
          <span>Sync Brain Settings</span>
        </button>
      </header>

      {/* Internal Tabs - Scrollable on Mobile */}
      <div className="flex space-x-4 border-b border-gray-800 overflow-x-auto no-scrollbar whitespace-nowrap">
        {['identity', 'playbook', 'pricing', 'knowledge'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-4 px-2 text-xs md:text-sm font-bold uppercase tracking-widest transition-all ${
              activeSection === tab ? 'text-pulse-gold border-b-2 border-pulse-gold' : 'text-gray-500 hover:text-gray-300'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-8">
        
        {/* SECTION 1: IDENTITY */}
        {activeSection === 'identity' && (
          <div className="bg-pulse-card rounded-xl border border-gray-800 p-5 md:p-8 space-y-6">
            <h3 className="text-lg md:text-xl font-bold text-white flex items-center space-x-2">
              <Info className="text-pulse-gold" size={20} />
              <span>Business Identity & Tone</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-500 uppercase">Business Name</label>
                <input type="text" className="w-full bg-pulse-dark border border-gray-700 rounded-lg p-3 text-white focus:border-pulse-gold outline-none text-sm" defaultValue="Luxe Glo Beauty & Spa" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-500 uppercase">Tone of Voice</label>
                <select className="w-full bg-pulse-dark border border-gray-700 rounded-lg p-3 text-white focus:border-pulse-gold outline-none text-sm">
                  <option>Premium & Persuasive (Senior Sales)</option>
                  <option>Friendly & Casual (Naija Vibe)</option>
                  <option>Direct & Professional</option>
                  <option>Pidgin First (Local Connector)</option>
                </select>
              </div>
              <div className="md:col-span-2 space-y-2">
                <label className="text-xs font-bold text-gray-500 uppercase">Competitive Edge (The Why)</label>
                <textarea className="w-full bg-pulse-dark border border-gray-700 rounded-lg p-3 text-white focus:border-pulse-gold outline-none h-24 text-sm" defaultValue="We use only imported organic oils from France. Our treatments are 90 mins, while others do 45 mins." />
              </div>
            </div>
          </div>
        )}

        {/* SECTION 2: PLAYBOOK */}
        {activeSection === 'playbook' && (
          <div className="bg-pulse-card rounded-xl border border-gray-800 p-5 md:p-8 space-y-6">
            <h3 className="text-lg md:text-xl font-bold text-white flex items-center space-x-2">
              <ShieldAlert className="text-pulse-gold" size={20} />
              <span>Objection Playbook</span>
            </h3>
            <div className="space-y-4">
              <div className="p-4 bg-pulse-dark rounded-lg border border-gray-700 flex justify-between items-start">
                <div className="space-y-1">
                  <p className="text-white font-bold text-sm">"It's too expensive"</p>
                  <p className="text-gray-400 text-xs italic">Pivot to the 90-min duration and premium French materials.</p>
                </div>
                <button className="text-gray-600 hover:text-red-400 transition-colors"><Trash2 size={16} /></button>
              </div>
              <button className="flex items-center space-x-2 text-pulse-gold font-bold text-sm hover:underline">
                <Plus size={16} />
                <span>Add Custom Response Rule</span>
              </button>
            </div>
          </div>
        )}

        {/* SECTION 3: PRICING */}
        {activeSection === 'pricing' && (
          <div className="bg-pulse-card rounded-xl border border-gray-800 p-5 md:p-8 space-y-6">
            <h3 className="text-lg md:text-xl font-bold text-white flex items-center space-x-2">
              <DollarSign className="text-pulse-gold" size={20} />
              <span>Revenue Boundaries</span>
            </h3>
            <div className="overflow-x-auto -mx-5 md:mx-0">
              <table className="w-full text-left min-w-[500px]">
                <thead>
                  <tr className="border-b border-gray-800">
                    <th className="py-4 px-5 md:px-0 text-xs font-bold text-gray-500 uppercase">Service</th>
                    <th className="py-4 text-xs font-bold text-gray-500 uppercase">Target</th>
                    <th className="py-4 text-xs font-bold text-gray-500 uppercase">Floor</th>
                    <th className="py-4 text-xs font-bold text-gray-500 uppercase">Action</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  <tr className="border-b border-gray-800 hover:bg-white/5 transition-colors">
                    <td className="py-4 px-5 md:px-0 font-medium">Full Body Glow</td>
                    <td className="py-4 text-white font-bold">₦45,000</td>
                    <td className="py-4 text-red-400 font-bold">₦38,000</td>
                    <td className="py-4"><button className="text-gray-600 hover:text-white"><Settings size={16} /></button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* SECTION 4: KNOWLEDGE */}
        {activeSection === 'knowledge' && (
          <div className="bg-pulse-card rounded-xl border border-gray-800 p-5 md:p-8 space-y-6">
            <h3 className="text-lg md:text-xl font-bold text-white flex items-center space-x-2">
              <MessageSquare className="text-pulse-gold" size={20} />
              <span>FAQs & Policies</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <label className="text-xs font-bold text-gray-500 uppercase">Knowledge Base (FAQs)</label>
                <div className="p-4 bg-pulse-dark border border-gray-700 rounded-lg h-32 overflow-y-auto text-sm text-gray-400">
                  "Do you offer home service?" {'->'} "Yes, for ₦5,000 extra."
                </div>
              </div>
              <div className="space-y-4">
                <label className="text-xs font-bold text-gray-500 uppercase">Hard Rules</label>
                <div className="p-4 bg-pulse-dark border border-gray-700 rounded-lg h-32 overflow-y-auto text-sm text-red-300">
                  - Never discount below the Floor Price.
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default BrainConfig;
