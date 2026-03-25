import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { UploadCloud, FileText, Briefcase, ChevronRight, Loader2, AlertCircle } from 'lucide-react';
import { analyzeResume } from '../services/api';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 15 },
  visible: { opacity: 1, y: 0, transition: { type: "spring", bounce: 0.4 } }
};

export default function UploadForm({ onAnalyze }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isHovering, setIsHovering] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setResumeFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription) {
      setError("Please provide both a resume file and a job description.");
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await analyzeResume(resumeFile, jobDescription);
      onAnalyze(data);
    } catch (err) {
      setError(err.message || "Failed to analyze resume.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-[0_8px_40px_rgba(0,0,0,0.04)] p-8 md:p-10 max-w-3xl mx-auto border border-white/50 relative overflow-hidden"
    >
      <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500"></div>
      
      <motion.div variants={itemVariants} className="flex items-center mb-8">
        <div className="bg-slate-100 p-3 rounded-2xl mr-4 shadow-inner">
          <UploadCloud className="w-7 h-7 text-slate-700" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Analysis Configuration</h2>
          <p className="text-sm text-slate-500 font-medium mt-1">Provide your documents below to begin.</p>
        </div>
      </motion.div>

      {error && (
        <motion.div 
          initial={{ opacity: 0, height: 0 }} 
          animate={{ opacity: 1, height: 'auto' }} 
          className="mb-8 bg-red-50 text-red-700 p-4 rounded-2xl border border-red-100 text-sm font-semibold flex items-center shadow-sm"
        >
          <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0" />
          {error}
        </motion.div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        <motion.div variants={itemVariants}>
          <label className="flex items-center text-sm font-bold text-slate-700 mb-3 uppercase tracking-wide">
            <FileText className="w-4 h-4 mr-2 text-indigo-500" />
            Resume Document (PDF/DOCX/TXT)
          </label>
          <div 
            className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all duration-300 relative group overflow-hidden ${isHovering ? 'border-indigo-500 bg-indigo-50/50' : 'border-slate-300 hover:border-indigo-400 hover:bg-slate-50'}`}
            onDragEnter={() => setIsHovering(true)}
            onDragLeave={() => setIsHovering(false)}
            onDrop={() => setIsHovering(false)}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            
            <UploadCloud className={`w-12 h-12 mx-auto mb-4 transition-colors ${resumeFile ? 'text-indigo-600' : 'text-slate-400 group-hover:text-indigo-500'}`} />
            
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
            />
            
            {resumeFile ? (
              <div className="text-indigo-700 font-semibold text-lg flex items-center justify-center">
                <FileText className="w-5 h-5 mr-2" />
                {resumeFile.name}
              </div>
            ) : (
              <div>
                <p className="text-slate-600 font-semibold mb-1">Drag and drop your resume here</p>
                <p className="text-slate-400 text-sm font-medium">or click to browse from your computer</p>
              </div>
            )}
          </div>
        </motion.div>

        <motion.div variants={itemVariants}>
          <label className="flex items-center text-sm font-bold text-slate-700 mb-3 uppercase tracking-wide">
            <Briefcase className="w-4 h-4 mr-2 text-blue-500" />
            Target Job Description
          </label>
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-2xl opacity-0 group-hover:opacity-10 transition duration-300"></div>
            <textarea
              rows="7"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="relative w-full p-5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all resize-none text-slate-700 font-medium leading-relaxed bg-white/50 backdrop-blur-sm"
              placeholder="Paste the target job requirements and responsibilities here. We'll cross-reference your resume against these..."
            ></textarea>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="pt-2">
          <button
            type="submit"
            disabled={loading}
            className="group w-full relative inline-flex items-center justify-center overflow-hidden rounded-2xl p-4 px-6 font-bold text-white bg-slate-900 transition-all shadow-[0_8px_20px_rgba(0,0,0,0.15)] hover:shadow-[0_8px_30px_rgba(30,58,138,0.3)] disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 opacity-90 group-hover:opacity-100 transition-opacity"></span>
            
            <span className="relative flex items-center justify-center w-full text-lg tracking-wide">
              {loading ? (
                <>
                  <Loader2 className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" />
                  Running Deep Analysis...
                </>
              ) : (
                <>
                  Commence Analysis
                  <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </span>
          </button>
        </motion.div>
      </form>
    </motion.div>
  );
}
