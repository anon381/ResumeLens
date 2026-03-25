import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Briefcase, FileText } from 'lucide-react';
import UploadForm from './components/UploadForm';
import MatchResults from './components/MatchResults';

function App() {
  const [results, setResults] = useState(null);

  return (
    <div className="min-h-screen bg-slate-50 relative text-slate-800 font-sans overflow-hidden">
      {/* Decorative background blobs */}
      <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-blue-400/20 rounded-full blur-[120px] mix-blend-multiply opacity-60 -translate-x-1/3 -translate-y-1/3 pointer-events-none"></div>
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-400/20 rounded-full blur-[100px] mix-blend-multiply opacity-60 translate-x-1/3 -translate-y-1/4 pointer-events-none"></div>

      <header className="relative z-10 pt-16 pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div 
            initial={{ opacity: 0, y: -20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ type: "spring", bounce: 0.5 }}
            className="inline-flex items-center justify-center p-3 bg-white/80 backdrop-blur-md rounded-2xl shadow-sm mb-6 border border-slate-200"
          >
            <div className="bg-blue-100 p-2.5 rounded-xl mr-3 shadow-inner">
              <Briefcase className="w-6 h-6 text-blue-700" />
            </div>
            <div className="bg-indigo-100 p-2.5 rounded-xl shadow-inner">
              <FileText className="w-6 h-6 text-indigo-700" />
            </div>
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900 mb-5 pb-2 bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900"
          >
            AI Resume Profiler
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="max-w-2xl mx-auto text-lg text-slate-500 font-medium leading-relaxed"
          >
            Instantly benchmark your resume against any job description. Uncover exact skill gaps and view your profile through the eyes of an ATS and a recruiter.
          </motion.p>
        </div>
      </header>
      
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
        <AnimatePresence mode="wait">
          {!results ? (
            <motion.div
              key="upload"
              initial={{ opacity: 0, scale: 0.97, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 1.03, filter: "blur(8px)" }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
            >
              <UploadForm onAnalyze={setResults} />
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 50, filter: "blur(10px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              <MatchResults results={results} onReset={() => setResults(null)} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
