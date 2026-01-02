import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Save, Globe, Shield, RefreshCw, Zap } from 'lucide-react';

const Config = () => {
    const [targetConfig, setTargetConfig] = useState({
        url: '',
        concurrency: 10,
        timeout: 5,
        evasion_level: 0
    });

    const [wafConfig, setWafConfig] = useState({
        type: 'modsecurity',
        log_path: ''
    });

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        fetchConfig();
    }, []);

    const fetchConfig = async () => {
        try {
            setLoading(true);
            const [targetRes, wafRes] = await Promise.all([
                axios.get('/api/v1/config/target'),
                axios.get('/api/v1/config/waf')
            ]);
            setTargetConfig({
                ...targetRes.data,
                evasion_level: targetRes.data.evasion_level || 0 // Default to 0 if missing
            });
            setWafConfig(wafRes.data);
        } catch (err) {
            console.error("Failed to load config", err);
            setMessage({ type: 'error', text: 'Failed to load configuration' });
        } finally {
            setLoading(false);
        }
    };

    const handleTargetChange = (e) => {
        const value = e.target.type === 'number' || e.target.type === 'range' ? parseInt(e.target.value) : e.target.value;
        setTargetConfig({ ...targetConfig, [e.target.name]: value });
    };

    const handleWafChange = (e) => {
        setWafConfig({ ...wafConfig, [e.target.name]: e.target.value });
    };

    const saveConfig = async () => {
        try {
            setSaving(true);
            setMessage(null);

            await Promise.all([
                axios.post('/api/v1/config/target', targetConfig),
                axios.post('/api/v1/config/waf', wafConfig)
            ]);

            setMessage({ type: 'success', text: 'Configuration saved successfully' });

            // Clear message after 3 seconds
            setTimeout(() => setMessage(null), 3000);
        } catch (err) {
            console.error("Failed to save", err);
            setMessage({ type: 'error', text: 'Failed to save configuration' });
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="flex h-64 items-center justify-center text-zinc-500">
                <RefreshCw className="animate-spin mr-2" /> Loading Configuration...
            </div>
        );
    }

    const getEvasionLabel = (level) => {
        switch (level) {
            case 0: return { label: 'None', desc: 'Raw payloads only', color: 'text-zinc-400' };
            case 1: return { label: 'Basic', desc: 'URL Encoding, Case Switching', color: 'text-yellow-500' };
            case 2: return { label: 'Advanced', desc: 'Double Encode, Comments, Whitespace', color: 'text-red-500' };
            default: return { label: 'Unknown', desc: '', color: 'text-zinc-500' };
        }
    }

    const evasionInfo = getEvasionLabel(targetConfig.evasion_level);

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h2 className="text-2xl font-bold text-white">System Configuration</h2>
                    <p className="text-zinc-400 mt-1">Manage target definitions and WAF parameters.</p>
                </div>
                {message && (
                    <div className={`px-4 py-2 rounded-lg text-sm font-medium ${message.type === 'success' ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-red-500/10 text-red-500 border border-red-500/20'
                        }`}>
                        {message.text}
                    </div>
                )}
            </div>

            <div className="grid gap-8">
                {/* Target Card */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl overflow-hidden">
                    <div className="px-6 py-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900/50">
                        <div className="flex items-center gap-3">
                            <Globe size={18} className="text-blue-500" />
                            <h3 className="font-semibold text-white">Target Definition</h3>
                        </div>
                        <span className="text-xs px-2 py-1 bg-blue-500/10 text-blue-400 rounded border border-blue-500/20">Active</span>
                    </div>
                    <div className="p-6 space-y-6">
                        <div className="grid grid-cols-2 gap-6">
                            <div className="col-span-2 space-y-2">
                                <label className="text-sm font-medium text-zinc-400">Target URL</label>
                                <input
                                    type="text"
                                    name="url"
                                    value={targetConfig.url}
                                    onChange={handleTargetChange}
                                    className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all font-mono"
                                    placeholder="http://example.com"
                                />
                            </div>
                        </div>

                        {/* Evasion Slider */}
                        <div className="space-y-4 p-4 bg-zinc-950/50 rounded-lg border border-zinc-800/50">
                            <div className="flex justify-between items-center">
                                <div className="flex items-center gap-2">
                                    <Zap size={16} className={evasionInfo.color} />
                                    <label className="text-sm font-medium text-zinc-300">Smart Evasion Level</label>
                                </div>
                                <div className="text-right">
                                    <span className={`text-sm font-bold ${evasionInfo.color}`}>{evasionInfo.label}</span>
                                    <p className="text-xs text-zinc-500">{evasionInfo.desc}</p>
                                </div>
                            </div>
                            <input
                                type="range"
                                name="evasion_level"
                                min="0"
                                max="2"
                                step="1"
                                value={targetConfig.evasion_level}
                                onChange={handleTargetChange}
                                className="w-full h-2 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-blue-600"
                            />
                            <div className="flex justify-between text-[10px] text-zinc-600 uppercase font-bold tracking-wider">
                                <span>None</span>
                                <span>Basic</span>
                                <span>Advanced</span>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-zinc-400">Concurrency</label>
                                <input
                                    type="number"
                                    name="concurrency"
                                    value={targetConfig.concurrency}
                                    onChange={handleTargetChange}
                                    className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all"
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-zinc-400">Timeout (s)</label>
                                <input
                                    type="number"
                                    name="timeout"
                                    value={targetConfig.timeout}
                                    onChange={handleTargetChange}
                                    className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all"
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* WAF Card */}
                <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl overflow-hidden">
                    <div className="px-6 py-4 border-b border-zinc-800 flex justify-between items-center bg-zinc-900/50">
                        <div className="flex items-center gap-3">
                            <Shield size={18} className="text-emerald-500" />
                            <h3 className="font-semibold text-white">WAF Adapter Settings</h3>
                        </div>
                        <span className="text-xs px-2 py-1 bg-emerald-500/10 text-emerald-400 rounded border border-emerald-500/20">Connected</span>
                    </div>
                    <div className="p-6 space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-zinc-400">Adapter Type</label>
                            <select
                                name="type"
                                value={wafConfig.type}
                                onChange={handleWafChange}
                                className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50"
                            >
                                <option value="modsecurity">ModSecurity (NGINX)</option>
                                <option value="aws">AWS WAF (Coming Soon)</option>
                                <option value="cloudflare">Cloudflare (Coming Soon)</option>
                            </select>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-zinc-400">Log Location</label>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    name="log_path"
                                    value={wafConfig.log_path}
                                    onChange={handleWafChange}
                                    className="flex-1 bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all font-mono text-sm"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="px-6 py-4 bg-zinc-900/30 border-t border-zinc-800 flex justify-end">
                        <button
                            onClick={saveConfig}
                            disabled={saving}
                            className={`flex items-center gap-2 px-6 py-2 bg-white text-black font-medium rounded-lg hover:bg-zinc-200 transition-colors ${saving ? 'opacity-70 cursor-wait' : ''}`}
                        >
                            {saving ? <RefreshCw className="animate-spin" size={16} /> : <Save size={16} />}
                            {saving ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default Config;
