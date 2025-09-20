import streamlit as st
import io
try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except Exception:
    PdfReader = None
    PDF_SUPPORT = False

# --- Page Configuration ---
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="✅",
    layout="wide"
)

# --- Custom CSS for Styling ---
# This CSS is adapted from your HTML to style the Streamlit components
# and achieve a similar dark theme.
st.markdown("""
<style>
    /* General body and font styles */
    body {
        font-family: 'Inter', sans-serif;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1f2937;
        border-right: 1px solid #374151;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #d1d5db;
    }
    [data-testid="stSidebar"] .stButton button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border-radius: 0.5rem;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #1d4ed8;
    }

    /* Verdict badges */
    .verdict-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        display: inline-block;
        margin-left: auto;
    }
    .verdict-high { background-color: #166534; color: #dcfce7; }
    .verdict-medium { background-color: #854d0e; color: #fef9c3; }
    .verdict-low { background-color: #991b1b; color: #fee2e2; }

    /* Skill tags */
    .skill-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        margin: 0.25rem;
    }
    .matched-skill { background-color: #1e40af; color: #dbeafe; }
    .missing-skill { background-color: #991b1b; color: #fee2e2; }

    /* Card for candidate display */
    .candidate-card {
        background-color: #1f2937;
        border-radius: 0.75rem;
        border: 1px solid #374151;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .candidate-card:hover {
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        border-color: #3b82f6;
    }

    /* Evidence box */
    .evidence {
        background-color: #111827;
        padding: 0.75rem;
        border-radius: 0.375rem;
        border: 1px solid #374151;
        font-style: italic;
        color: #d1d5db;
    }
    /* Progress bar inside candidate cards */
    .progress {
        background-color: #0f172a;
        border-radius: 0.375rem;
        height: 0.75rem;
        overflow: hidden;
        border: 1px solid #374151;
        margin: 0.5rem 0 0.75rem 0;
    }
    .progress-inner {
        height: 100%;
        background: linear-gradient(90deg,#34d399,#60a5fa);
    }
    details summary { cursor: pointer; color: #d1d5db; font-weight:600; }
</style>
""", unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
            <svg class="h-8 w-8 text-blue-500" style="height: 2rem; width: 2rem; color: #3b82f6;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <h1 style="font-size: 1.875rem; font-weight: 700;">Resume Analyzer</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 1. Job Description")

    # Initialize session state for job_description so we can update it when a file is uploaded
    if 'job_description' not in st.session_state:
        st.session_state['job_description'] = ""

    # Use tabs so user can switch between uploading a file and pasting text
    upload_tab, paste_tab = st.tabs(["Upload File", "Paste Text"])  # Upload File shown first by default

    with upload_tab:
        jd_file = st.file_uploader(
            "Upload a job description file (txt, md or pdf)",
            type=["txt", "md", "pdf"],
            accept_multiple_files=False,
            key="jd_file",
            label_visibility="collapsed"
        )

        # If the user uploads a file, read its contents and set it into session_state
        if jd_file is not None:
            try:
                raw = jd_file.read()
                name = getattr(jd_file, 'name', '') or ''
                lower_name = name.lower()
                is_pdf = lower_name.endswith('.pdf') or getattr(jd_file, 'type', '') == 'application/pdf'

                if is_pdf:
                    if PDF_SUPPORT:
                        try:
                            reader = PdfReader(io.BytesIO(raw))
                            text = ""
                            for p in reader.pages:
                                try:
                                    page_text = p.extract_text()
                                except Exception:
                                    page_text = None
                                if page_text:
                                    text += page_text + "\n"
                        except Exception as e:
                            st.error(f"Failed to read PDF: {e}")
                            text = ""
                    else:
                        st.error("PDF text extraction requires the `PyPDF2` package. Install with: `pip install PyPDF2`")
                        text = ""
                else:
                    # Try decoding as utf-8, fall back to latin-1 if needed
                    try:
                        text = raw.decode('utf-8') if isinstance(raw, (bytes, bytearray)) else str(raw)
                    except Exception:
                        text = raw.decode('latin-1') if isinstance(raw, (bytes, bytearray)) else str(raw)

                st.session_state['job_description'] = text
                st.success("Job description loaded from file.")
            except Exception as e:
                st.error(f"Could not read uploaded file: {e}")
    with paste_tab:
        job_description = st.text_area(
            "Paste the job description text here...",
            height=200,
            value=st.session_state.get('job_description', ''),
            key='job_description',
            label_visibility="collapsed"
        )

    # Number of jobs to analyze
    if 'num_jobs' not in st.session_state:
        st.session_state['num_jobs'] = 5

    num_jobs = st.number_input(
        "Number of jobs to evaluate:",
        min_value=1,
        max_value=100,
        value=st.session_state.get('num_jobs', 5),
        step=1,
        key='num_jobs'
    )

    st.markdown("## 2. Upload Resumes")
    uploaded_files = st.file_uploader(
        "Drag & drop PDF files here or click to browse",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    analyze_button = st.button("Analyze Resumes")


# --- Main Content ---

st.title('Analysis for "Senior Data Scientist"')
st.markdown('<p style="color: #9ca3af;">Showing matching candidates, sorted by relevance.</p>', unsafe_allow_html=True)

# This part of the code will run when the "Analyze Resumes" button is clicked.
# In a real application, you would process the `job_description` and `uploaded_files` here.
if analyze_button or uploaded_files:
    num_jobs = int(st.session_state.get('num_jobs', 5))
    uploaded_count = len(uploaded_files) if uploaded_files else 0

    if uploaded_count == 0:
        st.warning("No resumes uploaded — upload resume files to see matching candidates.")
    else:
        result_count = min(num_jobs, uploaded_count)
        for i in range(result_count):
            # Use the uploaded filename when available
            file_obj = uploaded_files[i]
            name = getattr(file_obj, 'name', f"Candidate_{i+1}.pdf")
            verdict_class = 'verdict-high' if i % 3 == 0 else ('verdict-medium' if i % 3 == 1 else 'verdict-low')
            verdict_text = "High" if verdict_class == 'verdict-high' else ("Medium" if verdict_class == 'verdict-medium' else "Low")
            pct = max(30, 95 - i * 10)
            card_html = f'''
            <div class="candidate-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0;">{name}</h3>
                    <span class="verdict-badge {verdict_class}">{verdict_text}</span>
                </div>
                <div class="progress"><div class="progress-inner" style="width:{pct}%;"></div></div>
                <details>
                    <summary>AI Deep Dive</summary>
                    <div style="margin-top:0.5rem;">
                        <div style="margin-bottom:0.5rem;"> 
                            <strong>✅ Matched Skills</strong>
                            <div style="margin-top:0.25rem;">
                                <span class="skill-tag matched-skill">Python</span>
                                <span class="skill-tag matched-skill">SQL</span>
                                <span class="skill-tag matched-skill">AWS</span>
                            </div>
                        </div>
                        <div style="margin-bottom:0.5rem;"> 
                            <strong>❌ Missing Skills</strong>
                            <div style="margin-top:0.25rem;">
                                <span class="skill-tag missing-skill">Kubernetes</span>
                                <span class="skill-tag missing-skill">Docker</span>
                            </div>
                        </div>
                        <div>
                            <strong>📄 Evidence from Experience</strong>
                            <p class="evidence">"Example evidence sentence describing relevant experience and outcome."</p>
                        </div>
                    </div>
                </details>
            </div>
            '''
            st.markdown(card_html, unsafe_allow_html=True)

else:
    st.info("Please upload resumes and click 'Analyze Resumes' to see the results.")

