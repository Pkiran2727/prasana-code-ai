import React, { useState } from 'react';
import { Wrench, Code2, Hash, FileJson, FileText, Lock, Copy, Check } from 'lucide-react';

export default function DevToolsCatalog() {
  const [selectedTool, setSelectedTool] = useState('json');
  const [inputVal, setInputVal] = useState('{"name":"Prasana","role":"developer"}');
  const [outputVal, setOutputVal] = useState('');
  const [copied, setCopied] = useState(false);

  const tools = [
    { id: 'json', name: 'JSON Formatter', icon: <FileJson className="w-4 h-4 text-cyan-400" /> },
    { id: 'base64', name: 'Base64 Encoder/Decoder', icon: <Code2 className="w-4 h-4 text-purple-400" /> },
    { id: 'markdown', name: 'Markdown Previewer', icon: <FileText className="w-4 h-4 text-emerald-400" /> },
    { id: 'hash', name: 'Hash & UUID Generator', icon: <Hash className="w-4 h-4 text-amber-400" /> }
  ];

  const handleProcess = () => {
    try {
      if (selectedTool === 'json') {
        const obj = JSON.parse(inputVal);
        setOutputVal(JSON.stringify(obj, null, 2));
      } else if (selectedTool === 'base64') {
        setOutputVal(btoa(inputVal));
      } else if (selectedTool === 'markdown') {
        setOutputVal(`Parsed Markdown Output:\n# ${inputVal}`);
      } else if (selectedTool === 'hash') {
        setOutputVal(`Generated UUID: ${crypto.randomUUID()}`);
      }
    } catch (e) {
      setOutputVal(`Error processing tool input: ${e.message}`);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(outputVal);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-full bg-ide-panel text-ide-text p-8 overflow-y-auto font-sans">
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold tracking-tight">Developer Tools & Utilities</h1>
          <p className="text-ide-muted text-sm mt-1">In-browser tools for JSON formatting, Base64 encoding, and hash generation.</p>
        </div>

        <div className="grid md:grid-cols-4 gap-4 mb-8">
          {tools.map(tool => (
            <button
              key={tool.id}
              onClick={() => setSelectedTool(tool.id)}
              className={`p-4 rounded-2xl border flex items-center gap-3 font-bold text-xs transition-all ${
                selectedTool === tool.id
                  ? 'bg-ide-sidebar border-cyan-500 text-ide-text shadow-lg shadow-cyan-500/10'
                  : 'bg-ide-panel border-ide-border text-ide-muted hover:text-ide-text'
              }`}
            >
              {tool.icon}
              <span>{tool.name}</span>
            </button>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-6 bg-ide-panel/80 border border-ide-border p-6 rounded-3xl">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-ide-muted mb-2">Input</label>
            <textarea
              rows={12}
              value={inputVal}
              onChange={e => setInputVal(e.target.value)}
              className="w-full bg-ide-bg border border-ide-border rounded-2xl p-4 font-mono text-xs text-cyan-200 focus:outline-none focus:border-cyan-500"
            />
            <button
              onClick={handleProcess}
              className="mt-3 px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-extrabold text-xs transition-all shadow-md"
            >
              Process Input
            </button>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-bold uppercase tracking-wider text-ide-muted">Output</label>
              {outputVal && (
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-1 text-[11px] text-cyan-400 hover:underline"
                >
                  {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copied!' : 'Copy'}</span>
                </button>
              )}
            </div>
            <textarea
              readOnly
              rows={12}
              value={outputVal}
              className="w-full bg-ide-bg border border-ide-border rounded-2xl p-4 font-mono text-xs text-emerald-300 focus:outline-none"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
