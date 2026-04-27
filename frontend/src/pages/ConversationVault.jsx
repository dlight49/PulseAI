import React, { useState, useEffect } from 'react';
import { 
  Search, 
  ChevronRight, 
  MessageCircle,
  ArrowLeft,
  Clock,
  ExternalLink
} from 'lucide-react';
import { getRecentChats, getChatHistory } from '../utils/api';

const ConversationVault = () => {
  const [selectedChat, setSelectedChat] = useState(null);
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const data = await getRecentChats('senior_sales_demo');
        setChats(data);
      } catch (err) {
        console.error("Failed to fetch chats:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchChats();
  }, []);

  const handleSelectChat = async (chat) => {
    setSelectedChat(chat);
    try {
      const history = await getChatHistory('senior_sales_demo', chat.contact_id);
      setMessages(history);
    } catch (err) {
      console.error("Failed to fetch message history:", err);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center h-[80vh]">
      <div className="w-8 h-8 border-4 border-pulse-gold border-t-transparent rounded-full animate-spin"></div>
    </div>
  );

  if (selectedChat) {
    return (
      <div className="h-full flex flex-col bg-pulse-dark animate-in slide-in-from-right duration-300">
        {/* Chat Header */}
        <header className="p-4 bg-pulse-card border-b border-gray-800 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center space-x-4">
            <button onClick={() => setSelectedChat(null)} className="text-gray-400 p-2 -ml-2">
              <ArrowLeft size={24} />
            </button>
            <div>
              <h3 className="text-white font-bold">{selectedChat.display_name || selectedChat.phone_number}</h3>
              <p className="text-xs text-green-400 font-medium tracking-wide">ACTIVE NEGOTIATION</p>
            </div>
          </div>
          <button className="text-pulse-gold p-2">
            <Clock size={20} />
          </button>
        </header>

        {/* Message Bubbles */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role.toUpperCase() === 'USER' ? 'justify-start' : 'justify-end'}`}>
              <div className={`max-w-[85%] p-4 rounded-2xl ${
                msg.role.toUpperCase() === 'USER' 
                  ? 'bg-gray-800 text-gray-200 rounded-bl-none' 
                  : 'bg-pulse-gold text-pulse-dark font-medium rounded-br-none shadow-lg'
              }`}>
                <p className="text-sm leading-relaxed">{msg.content}</p>
                <p className={`text-[10px] mt-1 ${msg.role.toUpperCase() === 'USER' ? 'text-gray-500' : 'text-pulse-dark opacity-60 text-right'}`}>
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Chat Footer (Info only) */}
        <footer className="p-4 bg-pulse-card border-t border-gray-800 text-center">
          <p className="text-xs text-gray-500 italic font-medium">Pulse AI is autonomously managing this lead.</p>
          <button className="mt-2 text-pulse-gold text-xs font-black uppercase tracking-widest flex items-center justify-center space-x-1 w-full py-2">
            <span>Take Over Conversation</span>
            <ExternalLink size={12} />
          </button>
        </footer>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 space-y-6">
      <header>
        <h2 className="text-2xl md:text-3xl font-bold text-white uppercase tracking-tighter">Conversation Vault</h2>
        <p className="text-gray-400 text-sm font-medium">Audit and monitor your AI's customer interactions.</p>
      </header>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={18} />
        <input 
          type="text" 
          placeholder="Search by name or phone..." 
          className="w-full bg-pulse-card border border-gray-800 rounded-xl py-3 pl-12 pr-4 text-white focus:border-pulse-gold outline-none text-sm transition-all"
        />
      </div>

      {/* Chat List */}
      <div className="space-y-2">
        {chats.map((chat) => (
          <button
            key={chat.contact_id}
            onClick={() => handleSelectChat(chat)}
            className="w-full bg-pulse-card p-4 rounded-xl border border-gray-800 hover:border-gray-600 transition-all flex items-center justify-between text-left group"
          >
            <div className="flex items-center space-x-4 overflow-hidden">
              <div className="w-12 h-12 rounded-full bg-pulse-dark flex items-center justify-center text-pulse-gold font-bold shrink-0 border border-gray-700">
                {(chat.display_name || chat.phone_number)[0]}
              </div>
              <div className="overflow-hidden">
                <div className="flex items-center space-x-2">
                   <p className="text-white font-bold text-sm truncate">{chat.display_name || chat.phone_number}</p>
                   <span className="text-[10px] bg-pulse-gold/10 text-pulse-gold px-2 py-0.5 rounded-full font-bold uppercase tracking-tighter">
                     NEGOTIATING
                   </span>
                </div>
                <p className="text-gray-400 text-xs truncate mt-0.5 italic">"{chat.last_message}"</p>
              </div>
            </div>
            <div className="flex flex-col items-end space-y-1 shrink-0 ml-4">
              <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest">
                {new Date(chat.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
              <ChevronRight className="text-gray-700 group-hover:text-pulse-gold transition-colors" size={18} />
            </div>
          </button>
        ))}
        {chats.length === 0 && (
          <div className="text-center py-20 bg-pulse-card/30 border border-dashed border-gray-800 rounded-xl">
             <p className="text-gray-600 font-bold uppercase tracking-widest italic">No active conversations yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationVault;
