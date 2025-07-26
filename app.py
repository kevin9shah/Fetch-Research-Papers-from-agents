import streamlit as st
from graph import graph
from qa_agent import answer_question
st.set_page_config(page_title="Agentic AI Research Assistant", layout="wide")

st.title("🧠 Agentic AI Research Assistant")

# User input: Research Topic
query = st.text_input("🔍 Enter your research topic")

# Initialize session state
if "papers" not in st.session_state:
    st.session_state.papers = []
if "final_state" not in st.session_state:
    st.session_state.final_state = {}
if "answered" not in st.session_state:
    st.session_state.answered = False

# Submit button
if st.button("Run Research Agent") and query:
    with st.spinner("Running the pipeline..."):
        initial_state = {
            "query": query,
            "status": "searching",
            "papers": [],
            "question": "",
            "answer": ""
        }
        final_state = graph.invoke(initial_state)
        st.session_state.final_state = final_state
        st.session_state.papers = final_state["papers"]
        st.session_state.answered = False

    st.success("✅ Papers retrieved and summarized!")

# Show papers
if st.session_state.papers:
    st.subheader("📄 Summarized Papers")
    for i, paper in enumerate(st.session_state.papers):
        with st.expander(f" Paper {i+1}: {paper['title']}"):
            st.markdown(f"** Authors:** {', '.join(paper['authors'])}")
            st.markdown(f"** Published:** {paper['published']}")
            st.markdown(f"** PDF:** [Link]({paper['pdf_url']})")
            st.markdown(f"** Summary:** {paper['simple_summary']}")

# Question box
if st.session_state.papers:
    st.subheader("Ask a question about the papers")
    question = st.text_input("❓ Your question")

    if st.button("Ask Gemini"):
        with st.spinner(" Thinking..."):
            answer = answer_question(st.session_state.papers, question)
            st.session_state.answered = True
            st.session_state.answer = answer

    if st.session_state.answered:
        st.markdown("###  Gemini's Answer")
        st.info(st.session_state.answer)
