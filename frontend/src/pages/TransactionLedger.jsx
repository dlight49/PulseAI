import React, { useState } from 'react';
import { 
  Download, 
  Filter, 
  Search, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  TrendingUp
} from 'lucide-react';

const TransactionLedger = () => {
  // Mock data for the ledger
  const transactions = [
    { id: '1', ref: 'pulse_a8b2c3d4', customer: 'Customer #8401', service: 'Full Body Glow', amount: '₦38,000', status: 'PAID', date: 'Oct 24, 10:15 AM' },
    { id: '2', ref: 'pulse_f1e2d3c4', customer: 'Customer #8405', service: 'Hydrating Facial', amount: '₦20,000', status: 'PENDING', date: 'Oct 24, 09:30 AM' },
    { id: '3', ref: 'pulse_x9y8z7w6', customer: 'Customer #8392', service: 'Mani-Pedi Combo', amount: '₦12,000', status: 'PAID', date: 'Oct 23, 04:45 PM' },
    { id: '4', ref: 'pulse_m5n4b3v2', customer: 'Customer #8388', service: 'Full Body Glow', amount: '₦45,000', status: 'FAILED', date: 'Oct 23, 01:20 PM' },
  ];

  const getStatusStyle = (status) => {
    switch (status) {
      case 'PAID': return 'bg-green-500/10 text-green-400 border-green-500/20';
      case 'PENDING': return 'bg-pulse-gold/10 text-pulse-gold border-pulse-gold/20';
      case 'FAILED': return 'bg-red-500/10 text-red-400 border-red-500/20';
      default: return 'bg-gray-500/10 text-gray-400';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'PAID': return <CheckCircle2 size={14} />;
      case 'PENDING': return <Clock size={14} />;
      case 'FAILED': return <AlertCircle size={14} />;
      default: return null;
    }
  };

  return (
    <div className="p-4 md:p-8 space-y-8 animate-in fade-in duration-500">
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-2xl md:text-3xl font-bold text-white uppercase tracking-tighter">Transaction Ledger</h2>
          <p className="text-gray-400 text-sm">Professional record of all AI-generated revenue.</p>
        </div>
        <button className="flex items-center space-x-2 bg-pulse-card border border-gray-800 text-gray-300 px-4 py-2 rounded-lg hover:bg-gray-800 transition-all text-sm w-full md:w-auto justify-center">
          <Download size={18} />
          <span>Export CSV</span>
        </button>
      </header>

      {/* Quick Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-pulse-card p-4 rounded-xl border border-gray-800">
          <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Today's Revenue</p>
          <p className="text-xl font-bold text-white">₦58,000</p>
        </div>
        <div className="bg-pulse-card p-4 rounded-xl border border-gray-800">
          <p className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Success Rate</p>
          <p className="text-xl font-bold text-green-400">92%</p>
        </div>
      </div>

      {/* Ledger Table / List */}
      <div className="bg-pulse-card rounded-xl border border-gray-800 overflow-hidden">
        <div className="p-4 border-b border-gray-800 flex flex-col md:flex-row justify-between gap-4">
           <div className="relative flex-1">
             <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
             <input type="text" placeholder="Search reference or customer..." className="w-full bg-pulse-dark border border-gray-700 rounded-lg py-2 pl-10 pr-4 text-xs text-white focus:border-pulse-gold outline-none" />
           </div>
           <button className="flex items-center space-x-2 bg-pulse-dark border border-gray-700 px-4 py-2 rounded-lg text-xs text-gray-400 hover:text-white transition-colors">
             <Filter size={16} />
             <span>All Statuses</span>
           </button>
        </div>

        {/* Desktop Table View */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-pulse-dark/50 text-[10px] font-bold text-gray-500 uppercase tracking-widest">
                <th className="px-6 py-4">Reference</th>
                <th className="px-6 py-4">Customer</th>
                <th className="px-6 py-4">Service</th>
                <th className="px-6 py-4">Amount</th>
                <th className="px-6 py-4">Status</th>
                <th className="px-6 py-4 text-right">Date</th>
              </tr>
            </thead>
            <tbody className="text-xs divide-y divide-gray-800">
              {transactions.map((tx) => (
                <tr key={tx.id} className="hover:bg-white/5 transition-colors group">
                  <td className="px-6 py-4 font-mono text-pulse-gold">{tx.ref}</td>
                  <td className="px-6 py-4 text-white font-medium">{tx.customer}</td>
                  <td className="px-6 py-4 text-gray-400">{tx.service}</td>
                  <td className="px-6 py-4 text-white font-bold">{tx.amount}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full border text-[10px] font-bold ${getStatusStyle(tx.status)}`}>
                      {getStatusIcon(tx.status)}
                      <span>{tx.status}</span>
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-500 text-right">{tx.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile List View */}
        <div className="md:hidden divide-y divide-gray-800">
          {transactions.map((tx) => (
            <div key={tx.id} className="p-4 space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-[10px] font-mono text-pulse-gold mb-1">{tx.ref}</p>
                  <p className="text-sm font-bold text-white">{tx.customer}</p>
                  <p className="text-xs text-gray-400">{tx.service}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-white">{tx.amount}</p>
                  <p className="text-[10px] text-gray-500 mt-1">{tx.date}</p>
                </div>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full border text-[10px] font-bold ${getStatusStyle(tx.status)}`}>
                  {getStatusIcon(tx.status)}
                  <span>{tx.status}</span>
                </span>
                <button className="text-xs text-pulse-gold font-bold underline">Details</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TransactionLedger;
