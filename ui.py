import streamlit as st

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
    # In a real app, you might use st.tabs for "Paste Text" and "Upload File"
    job_description = st.text_area(
        "Paste the job description text here...",
        height=200,
        value="""Senior Data Scientist

Responsibilities:
- Design and develop machine learning models...
- Work with large datasets using SQL and Python...

Required Skills:
- Python, SQL, AWS, Scikit-learn, TensorFlow, Kubernetes""",
        label_visibility="collapsed"
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
st.markdown('<p style="color: #9ca3af;">Showing 3 matching candidates, sorted by relevance.</p>', unsafe_allow_html=True)

# This part of the code will run when the "Analyze Resumes" button is clicked.
# In a real application, you would process the `job_description` and `uploaded_files` here.
if analyze_button or uploaded_files:
    # --- Candidate Card 1 (High Suitability) ---
    with st.container():
        st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.subheader("Aisha Sharma.pdf")
        with col2:
            st.markdown('<span class="verdict-badge verdict-high">High</span>', unsafe_allow_html=True)

        # Progress bar
        st.progress(92, text="92% Match")

        # Expander for details
        with st.expander("AI Deep Dive"):
            st.markdown("##### ✅ Matched Skills")
            st.markdown("""
                <span class="skill-tag matched-skill">Python</span>
                <span class="skill-tag matched-skill">SQL</span>
                <span class="skill-tag matched-skill">AWS</span>
                <span class="skill-tag matched-skill">Scikit-learn</span>
                <span class="skill-tag matched-skill">TensorFlow</span>
            """, unsafe_allow_html=True)

            st.markdown("##### ❌ Missing Skills")
            st.markdown('<span class="skill-tag missing-skill">Kubernetes</span>', unsafe_allow_html=True)

            st.markdown("##### 📄 Evidence from Experience")
            st.markdown(
                '<p class="evidence">"Led a project at FinSolve Technologies to develop a churn prediction model using Python and Scikit-learn, deployed on AWS, which improved retention by 12%."</p>',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Candidate Card 2 (Medium Suitability) ---
    with st.container():
        st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.subheader("Rohan Mehta_Resume.pdf")
        with col2:
            st.markdown('<span class="verdict-badge verdict-medium">Medium</span>', unsafe_allow_html=True)
        
        st.progress(76, text="76% Match")
        
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Candidate Card 3 (Low Suitability) ---
    with st.container():
        st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.subheader("Priya_CV_Final.pdf")
        with col2:
            st.markdown('<span class="verdict-badge verdict-low">Low</span>', unsafe_allow_html=True)
        
        st.progress(45, text="45% Match")
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Please upload resumes and click 'Analyze Resumes' to see the results.")

