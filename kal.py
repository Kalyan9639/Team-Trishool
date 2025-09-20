import streamlit as st
import time

# --- MOCK BACKEND LOGIC ---
# This function simulates the AI processing and returns the analysis results.
# In a real application, this would contain your resume parsing and scoring logic.
def run_analysis(job_description, resumes):
    # This is where you would process the job_description and uploaded resumes.
    # For now, we'll return a static list of results after a delay.
    print(f"Analyzing {len(resumes)} resumes for the role...")
    time.sleep(2) # Simulate processing time

    # This mock data represents the output of your AI model
    mock_results = [
        {
            "id": 1,
            "filename": "Aisha Sharma.pdf",
            "score": 92,
            "verdict": "High Suitability",
            "matched_skills": ["Python", "SQL", "AWS", "Scikit-learn", "TensorFlow"],
            "missing_skills": ["Kubernetes"],
            "evidence": "Led a project at FinSolve Technologies to develop a churn prediction model using Python and Scikit-learn, deployed on AWS, which improved retention by 12%."
        },
        {
            "id": 2,
            "filename": "Rohan Mehta_Resume.pdf",
            "score": 76,
            "verdict": "Medium Suitability",
            "matched_skills": ["Python", "SQL", "AWS"],
            "missing_skills": ["Scikit-learn", "TensorFlow", "Kubernetes"],
            "evidence": "Experience in data pipeline construction on AWS and proficient in SQL query optimization for large datasets."
        },
        {
            "id": 3,
            "filename": "Priya_CV_Final.pdf",
            "score": 45,
            "verdict": "Low Suitability",
            "matched_skills": ["Python"],
            "missing_skills": ["SQL", "AWS", "Scikit-learn", "TensorFlow", "Kubernetes"],
            "evidence": "Completed coursework in Python programming and introductory data structures. Lacks professional project experience in the required technologies."
        }
    ]
    return mock_results


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide"
)

# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Reset Streamlit's default theme */
    .stApp {
        background-color: #111827;
        color: #d1d5db;
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit's default footer and style the header */
    footer { visibility: hidden; }
    header {
        background-color: transparent !important;
        box-shadow: none !important;
    }
    
    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background-color: #1f2937;
        border-right: 1px solid #374151;
        padding: 1.5rem;
    }
    
    /* Custom classes from the HTML */
    .verdict-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .verdict-high { background-color: #166534; color: #dcfce7; }
    .verdict-medium { background-color: #854d0e; color: #fef9c3; }
    .verdict-low { background-color: #991b1b; color: #fee2e2; }

    .progress-bar {
        background-color: #374151;
        border-radius: 9999px;
        overflow: hidden;
        height: 0.625rem; /* h-2.5 */
        width: 100%;
    }
    .progress {
        height: 100%;
        border-radius: 9999px;
    }

    .card {
        background-color: #1f2937;
        border-radius: 0.75rem;
        border: 1px solid #374151;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: box-shadow 0.2s, border-color 0.2s;
    }
    .card:hover {
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        border-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)


# --- SESSION STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'results' not in st.session_state:
    st.session_state.results = []
if 'selected_candidate_id' not in st.session_state:
    st.session_state.selected_candidate_id = None


# --- URL-BASED NAVIGATION ---
try:
    query_params = st.query_params()
    if "page" in query_params:
        page = query_params["page"][0]
        candidate_id_str = query_params.get("id", [None])[0]
        candidate_id = int(candidate_id_str) if candidate_id_str is not None else None

        if st.session_state.page != page or st.session_state.selected_candidate_id != candidate_id:
            st.session_state.page = page
            st.session_state.selected_candidate_id = candidate_id
            st.experimental_set_query_params()
            st.experimental_rerun()
except:
    st.session_state.page = 'welcome'


# --- CALLBACKS for Button-based Navigation ---
def analyze_resumes_callback(jd, files):
    if not jd or not files:
        st.warning("Please provide a job description and at least one resume.")
        return
    with st.spinner("Analyzing..."):
        st.session_state.results = run_analysis(jd, files)
    st.session_state.page = 'results'


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <svg style="height: 2rem; width: 2rem; color: #3b82f6;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <h1 style="font-size: 1.5rem; font-weight: 700; color: #f9fafb;">Resume Analyzer</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.subheader("1. Job Description")
    job_description = st.text_area("Paste the job description here...", height=200, key="jd_input", 
    value="""Senior Data Scientist

Responsibilities:
- Design and develop machine learning models...
- Work with large datasets using SQL and Python...

Required Skills:
- Python, SQL, AWS, Scikit-learn, TensorFlow, Kubernetes""")

    st.subheader("2. Upload Resumes")
    uploaded_files = st.file_uploader("Drag & drop PDF files here or click to browse", accept_multiple_files=True, type="pdf")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.button("Analyze Resumes", use_container_width=True, type="primary", 
              on_click=analyze_resumes_callback, args=(job_description, uploaded_files))


# --- MAIN CONTENT ROUTER ---
if st.session_state.page == 'welcome':
    st.info("Please provide a job description and upload resumes in the sidebar, then click 'Analyze Resumes'.")

elif st.session_state.page == 'results':
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items-center; margin-bottom: 1.5rem;">
            <div>
                <h1 style="font-size: 1.875rem; font-weight: 700; color: #f9fafb;">Analysis for "Senior Data Scientist"</h1>
                <p style="color: #9ca3af; margin-top: 0.25rem;">Showing {} matching candidates, sorted by relevance.</p>
            </div>
        </div>
    """.format(len(st.session_state.results)), unsafe_allow_html=True)

    sorted_candidates = sorted(st.session_state.results, key=lambda x: x['score'], reverse=True)

    if not sorted_candidates:
        st.warning("Analysis complete, but no candidate data was found.")
    else:
        for candidate in sorted_candidates:
            verdict_class, progress_color, score_color = "", "#2563eb", "#60a5fa"
            if "High" in candidate["verdict"]: verdict_class = "verdict-high"
            elif "Medium" in candidate["verdict"]:
                verdict_class, progress_color, score_color = "verdict-medium", "#f59e0b", "#facc15"
            elif "Low" in candidate["verdict"]:
                verdict_class, progress_color, score_color = "verdict-low", "#ef4444", "#f87171"

            st.markdown(f"""
            <a href="?page=details&id={candidate['id']}" target="_self" style="text-decoration: none; color: inherit;">
                <div class="card">
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem;">
                        <div style="flex-grow: 1;">
                            <h3 style="font-weight: 700; font-size: 1.125rem; color: #f9fafb;">{candidate['filename']}</h3>
                            <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;">
                                <span style="font-weight: 600; color: {score_color}; font-size: 1.125rem;">{candidate['score']}%</span>
                                <div class="progress-bar">
                                    <div class="progress" style="width: {candidate['score']}%; background-color: {progress_color};"></div>
                                </div>
                            </div>
                        </div>
                        <div style="text-align: right; flex-shrink: 0; margin-left: 1rem;">
                            <span class="verdict-badge {verdict_class}">{candidate["verdict"]}</span>
                        </div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

elif st.session_state.page == 'details':
    candidate = next((c for c in st.session_state.results if c['id'] == st.session_state.selected_candidate_id), None)

    if candidate:
        st.markdown('<a href="?page=results" target="_self" style="text-decoration: none; color: #9ca3af; font-weight: 600;">← Back to List</a>', unsafe_allow_html=True)
        
        verdict_class, progress_color, score_color = "", "#2563eb", "#60a5fa"
        if "High" in candidate["verdict"]: verdict_class = "verdict-high"
        elif "Medium" in candidate["verdict"]:
            verdict_class, progress_color, score_color = "verdict-medium", "#f59e0b", "#facc15"
        elif "Low" in candidate["verdict"]:
            verdict_class, progress_color, score_color = "verdict-low", "#ef4444", "#f87171"

        matched_tags = "".join([f'<span style="background-color: rgba(59, 130, 246, 0.5); color: #93c5fd; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">{skill}</span>' for skill in candidate["matched_skills"]])
        missing_tags = "".join([f'<span style="background-color: rgba(239, 68, 68, 0.5); color: #fca5a5; padding: 0.25rem 0.5rem; border-radius: 0.25rem;">{skill}</span>' for skill in candidate["missing_skills"]])
        
        st.markdown(f"""
        <div class="card" style="margin-top: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="flex-grow: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="font-weight: 700; font-size: 1.125rem; color: #f9fafb;">{candidate['filename']}</h3>
                        <span class="verdict-badge {verdict_class}">{candidate['verdict']}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem;">
                        <span style="font-weight: 600; color: {score_color}; font-size: 1.125rem;">{candidate['score']}%</span>
                        <div class="progress-bar">
                            <div class="progress" style="width: {candidate['score']}%; background-color: {progress_color};"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #374151;">
                <h4 style="font-weight: 600; color: #d1d5db; margin-bottom: 0.75rem;">AI Deep Dive</h4>
                <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.5rem; font-size: 0.875rem;">
                    <div>
                        <h5 style="font-weight: 600; color: #9ca3af; margin-bottom: 0.5rem;">✅ Matched Skills</h5>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">{matched_tags}</div>
                    </div>
                    <div>
                        <h5 style="font-weight: 600; color: #9ca3af; margin-bottom: 0.5rem;">❌ Missing Skills</h5>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">{missing_tags}</div>
                    </div>
                    <div style="grid-column: span 2 / span 2;">
                        <h5 style="font-weight: 600; color: #9ca3af; margin-bottom: 0.5rem;">📄 Evidence from Experience</h5>
                        <p style="color: #d1d5db; background-color: #111827; padding: 0.75rem; border-radius: 0.375rem; border: 1px solid #374151; font-style: italic;">"{candidate['evidence']}"</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Could not find candidate details. Please go back to the list.")
        st.markdown('<a href="?page=results" target="_self" style="text-decoration: none; color: #9ca3af; font-weight: 600;">← Back to List</a>', unsafe_allow_html=True)

