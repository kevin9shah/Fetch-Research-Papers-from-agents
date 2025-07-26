from graph import graph
from qa_agent import answer_question_from_papers

def main():
    # Step 1: Get topic from user
    query = input("🔍 Enter research topic: ")
    
    # Step 2: Run the agentic pipeline
    initial_state = {
        "query": query,
        "status": "searching"
    }

    print("\n🤖 Running Research Assistant...")
    final_state = graph.invoke(initial_state)

    papers = final_state["papers"]

    # Step 3: Print summarized papers
    print("\n✅ Top Papers Found & Summarized:\n")
    for i, paper in enumerate(papers):
        print(f"\n📘 Paper {i+1}: {paper['title']}")
        print(f"👥 Authors: {', '.join(paper['authors'])}")
        print(f"📅 Published: {paper['published']}")
        print(f"🔗 PDF: {paper['pdf_url']}")
        print("🧠 Simple Summary:")
        print(paper["simple_summary"])
        print("=" * 100)

    # Step 4: Interactive Q&A
    print("\n🤖 You can now ask questions about the papers!")
    while True:
        question = input("\n❓ Ask a question (or type 'exit'): ")
        if question.lower() == "exit":
            print("👋 Exiting Research Assistant.")
            break

        answer = answer_question_from_papers(papers, question)
        print(f"\n🤖 Answer: {answer}")

if __name__ == "__main__":
    main()
