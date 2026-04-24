import React, { useState } from 'react';
import { 
  UserCheck, 
  ShieldCheck, 
  Target, 
  MoreVertical, 
  Plus, 
  MessageSquare,
  Lock,
  Zap
} from 'lucide-react';

const DestinyMode = () => {
  // Mock data for strategic contacts
  const [contacts, setContacts] = useState([
    { id: '1', name: 'Segun (Lead Investor)', type: 'INVESTOR', context: 'Values speed and growth metrics.', goal: 'Secure series A follow-on.' },
    { id: '2', name: 'Bolanle (Friend)', type: 'FRIEND', context: 'Close but asks for free favors.', goal: 'Maintain friendship + boundaries.' },
    { id: '3', name: 'Mr. Okafor (Angry Client)', type: 'CRITICAL', context: 'High value but unhappy with delay.', goal: 'De-escalate and preserve contract.' },
  ]);

  const getBadgeColor = (type) => {
    switch (type) {
      case 'INVESTOR': return 'text-pulse-gold bg-pulse-gold/10 border-pulse-gold/20';
      case 'CRITICAL': return 'text-red-400 bg-red-400/10 border-red-400/20';
      case 'FRIEND': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  return (
    <div className="p-4 md:p-8 space-y-8 animate-in fade-in duration-700">
      
      {/* Security Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 bg-pulse-card/50 p-6 rounded-2xl border border-pulse-gold/20 backdrop-blur-sm">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-pulse-gold/10 rounded-full border border-pulse-gold/30">
            <Lock className="text-pulse-gold" size={28} />
          </div>
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-white tracking-tight">DESTINY MODE</h2>
            <div className="flex items-center space-x-2">
              <Zap className="text-pulse-gold fill-pulse-gold" size={14} />
              <p className="text-pulse-gold text-xs font-bold uppercase tracking-widest">Personal Proxy Active</p>
            </div>
          </div>
        </div>
        <button className="flex items-center space-x-2 bg-pulse-gold text-pulse-dark font-bold px-6 py-3 rounded-xl shadow-[0_0_20px_rgba(241,196,15,0.2)] hover:scale-105 transition-all w-full md:w-auto justify-center">
          <Plus size={20} />
          <span>New Strategic Contact</span>
        </button>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 gap-6">
        <div className="flex items-center justify-between px-2">
          <h3 className="text-gray-400 text-sm font-bold uppercase tracking-widest">Strategic Contacts</h3>
          <p className="text-gray-600 text-xs">{contacts.length} Identities Monitored</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {contacts.map((contact) => (
            <div key={contact.id} className="bg-pulse-card p-6 rounded-2xl border border-gray-800 hover:border-pulse-gold/50 transition-all group relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4">
                <button className="text-gray-600 hover:text-white transition-colors">
                  <MoreVertical size={20} />
                </button>
              </div>

              {/* Status Header */}
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-12 h-12 rounded-full bg-pulse-dark flex items-center justify-center text-white font-bold text-lg border border-gray-700 group-hover:border-pulse-gold transition-colors">
                  {contact.name[0]}
                </div>
                <div>
                  <p className="text-white font-bold">{contact.name}</p>
                  <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded border ${getBadgeColor(contact.type)}`}>
                    {contact.type}
                  </span>
                </div>
              </div>

              {/* Intelligence Stats */}
              <div className="space-y-4">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2 text-gray-500">
                    <ShieldCheck size={14} />
                    <span className="text-[10px] font-bold uppercase tracking-tighter">Psychological Context</span>
                  </div>
                  <p className="text-xs text-gray-300 italic">"{contact.context}"</p>
                </div>

                <div className="space-y-1">
                  <div className="flex items-center space-x-2 text-pulse-gold">
                    <Target size={14} />
                    <span className="text-[10px] font-bold uppercase tracking-tighter uppercase">Proxy Mission</span>
                  </div>
                  <p className="text-sm text-white font-medium">{contact.goal}</p>
                </div>
              </div>

              {/* Actions */}
              <div className="mt-8 pt-6 border-t border-gray-800/50 flex justify-between items-center">
                <button className="flex items-center space-x-2 text-xs font-bold text-gray-500 hover:text-white transition-colors">
                  <MessageSquare size={14} />
                  <span>Audit History</span>
                </button>
                <button className="text-xs font-bold text-pulse-gold hover:underline">
                  Tweak DNA
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Global Proxy Rules */}
      <div className="bg-pulse-dark p-8 rounded-2xl border border-gray-800 space-y-6">
        <h3 className="text-white font-bold flex items-center space-x-2 uppercase tracking-widest text-sm">
          <Zap className="text-pulse-gold" size={18} />
          <span>Global Proxy Safeguards</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-pulse-card rounded-xl border border-gray-800 flex items-center justify-between">
            <span className="text-xs text-gray-400 font-medium italic">"Never admit to being an AI proxy."</span>
            <div className="w-8 h-4 bg-pulse-gold rounded-full relative"><div className="w-3 h-3 bg-pulse-dark rounded-full absolute right-0.5 top-0.5"></div></div>
          </div>
          <div className="p-4 bg-pulse-card rounded-xl border border-gray-800 flex items-center justify-between">
            <span className="text-xs text-gray-400 font-medium italic">"Always maintain high-status CEO posture."</span>
            <div className="w-8 h-4 bg-pulse-gold rounded-full relative"><div className="w-3 h-3 bg-pulse-dark rounded-full absolute right-0.5 top-0.5"></div></div>
          </div>
        </div>
      </div>

    </div>
  );
};

export default DestinyMode;
