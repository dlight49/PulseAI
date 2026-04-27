import React from 'react';
import { Rocket, Shield, Zap, MessageSquare, ArrowRight } from 'lucide-react';

const LandingPage = ({ onStartTrial, onLogin }) => {
  return (
    <div className="min-h-screen bg-pulse-dark text-pulse-text selection:bg-pulse-gold selection:text-pulse-dark">
      {/* NAVIGATION */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <h1 className="text-2xl font-black text-pulse-gold tracking-tighter">PULSE AI</h1>
        <div className="space-x-8 flex items-center">
          <button onClick={onLogin} className="text-sm font-medium hover:text-pulse-gold transition-colors">LOGIN</button>
          <button 
            onClick={onStartTrial}
            className="bg-pulse-gold text-pulse-dark px-6 py-2 rounded-full font-bold text-sm hover:scale-105 transition-transform shadow-[0_0_20px_rgba(241,196,15,0.3)]"
          >
            START FREE TRIAL
          </button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <header className="max-w-7xl mx-auto px-8 py-24 text-center space-y-8">
        <div className="inline-flex items-center space-x-2 bg-pulse-card px-4 py-2 rounded-full border border-gray-800 animate-bounce">
          <Zap size={16} className="text-pulse-gold" />
          <span className="text-xs font-bold tracking-widest uppercase">The Future of Sales is AI</span>
        </div>
        <h2 className="text-6xl md:text-8xl font-black tracking-tighter max-w-4xl mx-auto leading-tight">
          YOUR BUSINESS ON <span className="text-pulse-gold">AUTOPILOT.</span>
        </h2>
        <p className="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto font-medium">
          Deploy an elite digital workforce that closes sales, handles objections, and grows your revenue 24/7 on WhatsApp.
        </p>
        <div className="flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-6 pt-8">
          <button 
            onClick={onStartTrial}
            className="w-full md:w-auto bg-pulse-gold text-pulse-dark px-10 py-5 rounded-2xl font-black text-lg flex items-center justify-center space-x-3 hover:scale-105 transition-all shadow-[0_0_30px_rgba(241,196,15,0.4)]"
          >
            <span>START 7-DAY TRIAL</span>
            <ArrowRight size={20} />
          </button>
          <button className="w-full md:w-auto bg-transparent border border-gray-800 px-10 py-5 rounded-2xl font-bold text-lg hover:bg-pulse-card transition-colors">
            VIEW DEMO
          </button>
        </div>
      </header>

      {/* FEATURES GRID */}
      <section className="max-w-7xl mx-auto px-8 py-24 grid md:grid-cols-3 gap-8">
        {[
          {
            icon: <MessageSquare className="text-pulse-gold" size={32} />,
            title: "WhatsApp Native",
            desc: "Direct integration with WhatsApp Business API. No hacks, just pure performance."
          },
          {
            icon: <Shield className="text-pulse-gold" size={32} />,
            title: "Executive Intelligence",
            desc: "Not just a chatbot. An AI that understands your business DNA and negotiates like a pro."
          },
          {
            icon: <Rocket className="text-pulse-gold" size={32} />,
            title: "7-Day Trial",
            desc: "Full access for 7 days. Experience the revenue growth before you pay a single kobo."
          }
        ].map((f, i) => (
          <div key={i} className="bg-pulse-card p-10 rounded-3xl border border-gray-800 hover:border-pulse-gold/50 transition-colors group">
            <div className="mb-6 group-hover:scale-110 transition-transform">{f.icon}</div>
            <h3 className="text-2xl font-bold mb-4">{f.title}</h3>
            <p className="text-gray-400 leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </section>

      {/* FOOTER */}
      <footer className="border-t border-gray-800 py-12 text-center text-gray-500 text-sm">
        <p>© 2026 PULSE AI. All Rights Reserved. Built for PrimeStyle.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
