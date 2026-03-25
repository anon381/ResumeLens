const API_URL = 'http://localhost:8000/api';

export async function parseResumeFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/upload-resume`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to parse resume');
  }

  return response.json();
}

export async function analyzeResume(file, jobDescription) {
  // First extract text from resume
  const parseResult = await parseResumeFile(file);
  const resumeText = parseResult.data.raw_text;

  // Then analyze it
  const formData = new FormData();
  formData.append('resume_text', resumeText);
  formData.append('job_description', jobDescription);

  const response = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Analysis failed');
  }

  return response.json();
}
