import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, Zap, CheckCircle, MessageSquare } from 'lucide-react';
import { getBusinessSummary } from '../utils/api';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getBusinessSummary('senior_sales_demo');
        setMetrics(data);
      } catch (err) {
        console.error("Failed to fetch live metrics:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  const stats = metrics ? [
    { label: 'Total Revenue Generated', value: `₦${metrics.total_revenue.toLocaleString()}`, icon: TrendingUp, trend: '+12.5%' },
    { label: 'AI Successful Closes', value: metrics.deals_closed.toString(), icon: CheckCircle, trend: '+8%' },
    { label: 'Active Conversations', value: metrics.active_conversations.toString(), icon: MessageSquare, trend: '+22%' },
    { label: 'Brain Efficiency', value: '98.2%', icon: Zap, trend: '+0.5%' },
  ] : [];

  if (loading) return (
    <div className="flex items-center justify-center h-[80vh]">
      <div className="w-8 h-8 border-4 border-pulse-gold border-t-transparent rounded-full animate-spin"></div>
    </div>
  );

  return (
    <div className="p-4 md:p-8 space-y-8 animate-in fade-in duration-500">
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-white">ROI Command Center</h2>
          <p className="text-gray-400 text-sm md:text-base">Monitoring your digital sales workforce in real-time.</p>
        </div>
        <div className="bg-pulse-card px-4 py-2 rounded-lg border border-gray-800 flex items-center space-x-2 w-full md:w-auto justify-center">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs font-bold text-gray-300 tracking-widest uppercase">System Online</span>
        </div>
      </header>

      {/* Stats Grid - Stacked on Mobile, 2 per row on tablet, 4 on desktop */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-pulse-card p-5 md:p-6 rounded-xl border border-gray-800 hover:border-pulse-gold transition-colors group">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-pulse-dark rounded-lg group-hover:bg-pulse-gold group-hover:text-pulse-dark transition-colors">
                <stat.icon size={20} />
              </div>
              <span className="text-xs font-bold text-green-400">{stat.trend}</span>
            </div>
            <p className="text-gray-400 text-xs md:text-sm font-medium">{stat.label}</p>
            <p className="text-xl md:text-2xl font-bold text-white mt-1">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Bottom Section - Vertical on Mobile */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Live Closing Feed */}
        <div className="lg:col-span-2 bg-pulse-card rounded-xl border border-gray-800 p-5 md:p-6">
          <h3 className="text-lg md:text-xl font-bold text-white mb-6">Live Closing Feed</h3>
          <div className="space-y-3">
            {[1, 2, 3, 4].map((item) => (
              <div key={item} className="flex items-center justify-between p-3 md:p-4 bg-pulse-dark rounded-lg border border-gray-800 hover:border-gray-700 transition-colors">
                <div className="flex items-center space-x-3 md:space-x-4 overflow-hidden">
                  <div className="w-8 h-8 md:w-10 md:h-10 shrink-0 rounded-full bg-gray-800 flex items-center justify-center text-pulse-gold text-xs md:text-sm font-bold">
                    C
                  </div>
                  <div className="truncate">
                    <p className="text-white font-bold text-xs md:text-sm truncate">Customer #{8400 + item}</p>
                    <p className="text-gray-500 text-[10px] md:text-xs">Full Body Glow</p>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <p className="text-pulse-gold font-bold text-xs md:text-sm">₦38,000</p>
                  <p className="text-[10px] md:text-xs text-green-400 font-medium italic">Closing...</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Config */}
        <div className="bg-pulse-card rounded-xl border border-gray-800 p-6">
          <h3 className="text-xl font-bold text-white mb-6">Quick Brain Check</h3>
          <div className="space-y-6">
            <div className="p-4 bg-pulse-dark rounded-lg border border-gray-800">
              <p className="text-xs text-gray-500 font-bold uppercase mb-2">Active Persona</p>
              <p className="text-white font-medium">Senior Sales Lead (V5.0)</p>
            </div>
            <div className="p-4 bg-pulse-dark rounded-lg border border-gray-800">
              <p className="text-xs text-gray-500 font-bold uppercase mb-2">Revenue Guard</p>
              <p className="text-white font-medium italic">"Never below floor price"</p>
            </div>
            <button className="w-full bg-pulse-gold text-pulse-dark font-bold py-3 rounded-lg hover:brightness-110 transition-all shadow-lg">
              Tweak Brain Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
