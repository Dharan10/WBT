import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FileText, Download, Eye, Calendar, HardDrive, FileJson, FileType } from 'lucide-react';

const Reports = () => {
    const [reports, setReports] = useState([]);
    const [selectedReport, setSelectedReport] = useState(null);

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            const res = await axios.get('/api/v1/reports');
            setReports(res.data.map(r => ({
                id: r.name,
                name: r.name,
                date: new Date(r.modified * 1000).toLocaleString(),
                size: (r.size / 1024).toFixed(2) + ' KB',
                type: r.name.endsWith('.pdf') ? 'pdf' : 'json'
            })));
        } catch (err) {
            console.error("Failed to load reports");
        }
    };

    const handleAction = (filename, action) => {
        const url = `/api/v1/reports/${filename}`;
        if (action === 'view') {
            if (filename.endsWith('.json')) {
                // optimized fetch for viewing json
                axios.get(url).then(res => {
                    setSelectedReport({ name: filename, content: JSON.stringify(res.data, null, 2) });
                });
            } else {
                window.open(url, '_blank');
            }
        } else {
            // Force download trick
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
        }
    };

    return (
        <div className="max-w-7xl mx-auto h-[calc(100vh-140px)] flex gap-6">
            <div className={`flex-1 transition-all ${selectedReport ? 'w-1/2' : 'w-full'}`}>
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h2 className="text-2xl font-bold text-white">Reports Library</h2>
                        <p className="text-zinc-400 mt-1">Audit artifacts and executive summaries.</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                    {reports.map((r) => (
                        <div key={r.id} className="group bg-zinc-900/50 border border-zinc-800 rounded-xl p-4 hover:border-blue-500/30 hover:bg-zinc-800/30 transition-all">
                            <div className="flex items-start gap-4">
                                <div className={`p-3 rounded-lg ${r.type === 'pdf' ? 'bg-rose-500/10 text-rose-500' : 'bg-amber-500/10 text-amber-500'}`}>
                                    {r.type === 'pdf' ? <FileType size={24} /> : <FileJson size={24} />}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <h4 className="font-semibold text-zinc-200 truncate" title={r.name}>{r.name}</h4>
                                    <div className="flex items-center gap-4 mt-2 text-xs text-zinc-500">
                                        <div className="flex items-center gap-1.5">
                                            <Calendar size={12} />
                                            <span>{r.date}</span>
                                        </div>
                                        <div className="flex items-center gap-1.5">
                                            <HardDrive size={12} />
                                            <span>{r.size}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="mt-4 flex gap-2">
                                <button
                                    onClick={() => handleAction(r.name, 'view')}
                                    className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-lg text-sm font-medium transition-colors"
                                >
                                    <Eye size={16} />
                                    View
                                </button>
                                <button
                                    onClick={() => handleAction(r.name, 'download')}
                                    className="px-3 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-lg transition-colors border-l border-zinc-700"
                                    title="Download"
                                >
                                    <Download size={16} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Preview Panel */}
            {selectedReport && (
                <div className="w-1/2 bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden flex flex-col shadow-2xl">
                    <div className="px-4 py-3 border-b border-zinc-800 bg-zinc-950 flex justify-between items-center">
                        <span className="font-mono text-sm text-zinc-300">{selectedReport.name}</span>
                        <button onClick={() => setSelectedReport(null)} className="text-zinc-500 hover:text-white">
                            Close
                        </button>
                    </div>
                    <div className="flex-1 overflow-auto p-4 bg-zinc-950 text-xs font-mono text-zinc-300">
                        <pre>{selectedReport.content}</pre>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Reports;
