"""
Streamlit Web Frontend for Research Assistant
Allows uploading documents (.pdf, .docx, .txt, .md), indexing them into RAG,
asking research questions, visualizing data, and downloading generated reports.
"""
import os
import streamlit as st

from config.settings import settings
from rag.retriever import DocumentRetriever
from agents.research_agent import ResearchAgent
from agents.visualization_agent import VisualizationAgent
from agents.report_agent import ReportAgent

# Set page layout & title
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    .doc-card {
        padding: 10px;
        border-radius: 6px;
        background-color: #f8f9fa;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def ensure_directories():
    os.makedirs(settings.DOCS_DIR, exist_ok=True)
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_DIR, exist_ok=True)


def save_uploaded_files(uploaded_files) -> list[str]:
    saved_paths = []
    ensure_directories()
    for file in uploaded_files:
        path = os.path.join(settings.DOCS_DIR, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(file.name)
    return saved_paths


def get_existing_documents() -> list[str]:
    ensure_directories()
    if not os.path.exists(settings.DOCS_DIR):
        return []
    supported = {".pdf", ".docx", ".txt", ".md"}
    return [
        f for f in os.listdir(settings.DOCS_DIR)
        if os.path.splitext(f)[1].lower() in supported
    ]


def main():
    ensure_directories()

    # --- Sidebar ---
    st.sidebar.title("🔬 Research Assistant")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📄 Document Management")
    st.sidebar.write("Upload documents to ingest into RAG vector store:")

    uploaded_files = st.sidebar.file_uploader(
        "Attach Documents",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        help="Upload PDF, DOCX, TXT, or Markdown files"
    )

    if uploaded_files:
        if st.sidebar.button("💾 Save & Ingest Uploaded Files", use_container_width=True):
            with st.spinner("Saving & Indexing uploaded documents..."):
                saved_names = save_uploaded_files(uploaded_files)
                retriever = DocumentRetriever()
                num_chunks = retriever.ingest_directory(settings.DOCS_DIR)
                st.sidebar.success(f"Indexed {len(saved_names)} file(s) ({num_chunks} chunks)!")

    # Existing Documents List
    existing_docs = get_existing_documents()
    if existing_docs:
        with st.sidebar.expander(f"📁 Indexed Documents ({len(existing_docs)})", expanded=False):
            for doc in existing_docs:
                st.write(f"- `{doc}`")
            if st.button("🔄 Re-index All Documents", use_container_width=True):
                with st.spinner("Re-indexing document folder..."):
                    retriever = DocumentRetriever()
                    num_chunks = retriever.ingest_directory(settings.DOCS_DIR)
                    st.success(f"Successfully re-indexed {num_chunks} chunks!")
    else:
        st.sidebar.info("No documents in `data/documents/` yet.")

    # --- Main Content Area ---
    st.markdown('<div class="main-header">Multi-Agent AI Research Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Retrieval-Augmented Generation (RAG) + Live Web Search + Automatic Data Visualization</div>',
        unsafe_allow_html=True
    )

    # Question Input
    user_query = st.text_area(
        "Enter your research topic or question:",
        height=100,
        placeholder="e.g. Summarize the main points from the uploaded documents and visualize key findings..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_research = st.button("🚀 Run Research", type="primary", use_container_width=True)

    if run_research:
        if not user_query.strip():
            st.warning("Please enter a research question first.")
            return

        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
            st.error("Please configure your Groq API Key in `.env`.")
            return

        # Execute Multi-Agent Workflow
        st.markdown("### 📊 Research Execution")

        # Step 1: Research Agent
        with st.status("🔍 Step 1/3: Researching documents & web sources...", expanded=True) as status1:
            try:
                research = ResearchAgent().run(user_query)
                status1.update(label="✅ Research completed!", state="complete", expanded=False)
            except Exception as e:
                status1.update(label="❌ Research agent failed.", state="error")
                st.error(f"Error during research: {e}")
                return

        # Step 2: Visualization Agent
        with st.status("📈 Step 2/3: Checking & generating visualizations...", expanded=True) as status2:
            try:
                viz = VisualizationAgent().run(research.answer, user_query)
                if viz.created:
                    status2.update(label=f"✅ Visualization generated ({viz.chart_type})!", state="complete", expanded=False)
                else:
                    status2.update(label=f"ℹ️ No chart needed ({viz.reason})", state="complete", expanded=False)
            except Exception as e:
                status2.update(label="⚠️ Visualization attempt skipped.", state="complete", expanded=False)
                st.warning(f"Visualization notice: {e}")
                viz = None

        # Step 3: Report Agent
        with st.status("📄 Step 3/3: Compiling final research report...", expanded=True) as status3:
            try:
                report_path = ReportAgent().build(user_query, research, viz)
                status3.update(label="✅ Report compiled successfully!", state="complete", expanded=False)
            except Exception as e:
                status3.update(label="❌ Report generation failed.", state="error")
                st.error(f"Error building report: {e}")
                report_path = None

        st.markdown("---")

        # Display Results
        res_col, viz_col = st.columns([3, 2])

        with res_col:
            st.subheader("💡 Research Findings")
            st.markdown(research.answer)

        with viz_col:
            if viz and viz.created and viz.path and os.path.exists(viz.path):
                st.subheader("📊 Visualization")
                st.image(viz.path, caption=f"Chart type: {viz.chart_type}", use_column_width=True)

        # Report Download Section
        if report_path and os.path.exists(report_path):
            st.markdown("---")
            st.subheader("📥 Export Report")
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()

            st.download_button(
                label="📥 Download Full Report (Markdown)",
                data=report_content,
                file_name="research_report.md",
                mime="text/markdown"
            )


if __name__ == "__main__":
    main()
