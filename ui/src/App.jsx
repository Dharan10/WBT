import React, { useState } from 'react';
import {
  LayoutDashboard,
  ShieldCheck,
  Settings,
  FileText,
  Menu,
  Activity,
  Zap,
  Book,
} from 'lucide-react';
import Dashboard from './components/Dashboard';
import Config from './components/Config';
import Reports from './components/Reports';
import Docs from './components/Docs';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return <Dashboard setActiveTab={setActiveTab} />;
      case 'config': return <Config />;
      case 'reports': return <Reports />;
      case 'docs': return <Docs />; // New Route
      default: return <Dashboard setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="flex h-screen bg-[#09090b] text-zinc-100 font-sans overflow-hidden selection:bg-blue-500/30">
      {/* Sidebar */}
      <motion.aside
        initial={{ width: 260 }}
        animate={{ width: isSidebarOpen ? 280 : 80 }}
        className="border-r border-zinc-800 bg-zinc-900/50 backdrop-blur-xl flex flex-col z-20"
      >
        <div className="h-20 flex items-center px-6 border-b border-zinc-800/50 gap-4">
          <div className="relative group cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="absolute inset-0 bg-indigo-500 blur-lg opacity-40 group-hover:opacity-60 transition-opacity rounded-xl"></div>
            <div className="relative p-2.5 bg-gradient-to-br from-indigo-600 via-blue-600 to-sky-600 rounded-xl shadow-inner border border-white/10">
              <Zap className="w-6 h-6 text-white text-shadow-sm" fill="currentColor" />
            </div>
          </div>
          {isSidebarOpen && (
            <div className="flex flex-col cursor-pointer" onClick={() => setActiveTab('dashboard')}>
              <span className="font-bold text-xl tracking-tight text-white font-display">WBT</span>
              <span className="text-[10px] uppercase tracking-wider text-zinc-500 font-bold">Framework v2</span>
            </div>
          )}
        </div>

        <nav className="flex-1 p-4 space-y-2 mt-4">
          <NavButton
            active={activeTab === 'dashboard'}
            onClick={() => setActiveTab('dashboard')}
            icon={<LayoutDashboard size={22} />}
            label="Overview"
            expanded={isSidebarOpen}
          />
          <NavButton
            active={activeTab === 'reports'}
            onClick={() => setActiveTab('reports')}
            icon={<FileText size={22} />}
            label="Audit Reports"
            expanded={isSidebarOpen}
          />
          <div className="my-4 border-t border-zinc-800/50 mx-2"></div>
          <NavButton
            active={activeTab === 'config'}
            onClick={() => setActiveTab('config')}
            icon={<Settings size={22} />}
            label="System Config"
            expanded={isSidebarOpen}
          />
          <NavButton
            active={activeTab === 'docs'}
            onClick={() => setActiveTab('docs')}
            icon={<Book size={22} />}
            label="Documentation"
            expanded={isSidebarOpen}
          />
        </nav>

        <div className="p-4 border-t border-zinc-800 bg-zinc-900/30">
          <div className={`flex items-center gap-3 px-3 py-3 rounded-xl bg-zinc-950/50 border border-zinc-800/50 hover:border-zinc-700 transition-colors cursor-pointer ${!isSidebarOpen && 'justify-center'}`}>
            <div className="relative">
              <span className="absolute inset-0 rounded-full animate-ping bg-emerald-500/20"></span>
              <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full shadow-[0_0_8px_rgba(16,185,129,0.5)]"></div>
            </div>
            {isSidebarOpen && (
              <div className="flex flex-col">
                <span className="text-xs font-semibold text-zinc-300">Engine Active</span>
                <span className="text-[10px] text-zinc-500">Latency: 12ms</span>
              </div>
            )}
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 bg-[#09090b] relative">
        {/* Top Header */}
        <header className="h-20 border-b border-zinc-800 bg-zinc-900/30 backdrop-blur-md flex items-center justify-between px-8 z-10">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-zinc-800 rounded-lg text-zinc-400 hover:text-white transition-colors"
            >
              <Menu size={20} />
            </button>
            <div className="h-6 w-px bg-zinc-800"></div>
            <h1 className="text-lg font-semibold text-zinc-200">
              {activeTab === 'dashboard' ? 'Traffic Overview' :
                activeTab === 'config' ? 'System Configuration' :
                  activeTab === 'docs' ? 'Documentation' : 'Audit Records'}
            </h1>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/5 border border-emerald-500/20 text-emerald-500 text-xs font-medium">
              <ShieldCheck size={14} />
              <span>Protection Active</span>
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-auto p-8 relative scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent">
          {/* Background Decor */}
          <div className="absolute top-0 left-0 w-full h-[500px] bg-gradient-to-b from-blue-900/5 via-indigo-900/5 to-transparent pointer-events-none" />

          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10, scale: 0.99 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.99 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="relative z-10 max-w-[1600px] mx-auto"
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

const NavButton = ({ active, onClick, icon, label, expanded }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center gap-4 px-3 py-3 rounded-xl transition-all duration-200 group relative ${active
      ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20'
      : 'text-zinc-400 hover:bg-zinc-800/80 hover:text-zinc-200'
      } ${!expanded && 'justify-center'}`}
  >
    {React.cloneElement(icon, { size: expanded ? 20 : 22, className: active ? 'text-white' : 'text-zinc-500 group-hover:text-zinc-300' })}

    {expanded ? (
      <span className="text-sm font-medium tracking-wide">{label}</span>
    ) : (
      <div className="absolute left-full ml-4 px-3 py-1.5 bg-zinc-900 text-white text-xs font-medium rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 border border-zinc-800 shadow-xl transition-opacity">
        {label}
        {/* Arrow */}
        <div className="absolute top-1/2 -left-1 -mt-1 border-4 border-transparent border-r-zinc-900"></div>
      </div>
    )}
  </button>
);

export default App;
