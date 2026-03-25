import requests
import json

URL_UPLOAD = "http://localhost:8000/api/upload-resume"
URL_ANALYZE = "http://localhost:8000/api/analyze"

print("--- Simulating Frontend Web Request ---")

# 1. Upload via file
print("1. Uploading document as User...")
files = {'file': open('../sample_resume.txt', 'rb')}
upload_resp = requests.post(URL_UPLOAD, files=files)
upload_data = upload_resp.json()
parsed_text = upload_data['data']['raw_text']
print(f"-> Parsed Text Length: {len(parsed_text)} characters")

# 2. Analyze via form-data
print("\n2. Sending Extracted Text + User JD to /api/analyze ...")
with open('../sample_jd.txt', 'r') as f:
    jd_text = f.read()

payload = {
    'resume_text': parsed_text,
    'job_description': jd_text
}
analyze_resp = requests.post(URL_ANALYZE, data=payload)
results = analyze_resp.json()

print("\n--- RESULTS FROM BACKEND ENDPOINT ---")
print(f"Overall Match Score: {results['match_score']}%")
print(f"ATS Score: {results['ats_score']}%")
print(f"Key Suggestions: {len(results['suggestions'])}")
print("End-to-End API is working dynamically!")