
import os
from typing import TypedDict

from dotenv import load_dotenv
from google import genai
from langgraph.graph import StateGraph, START, END


# Load environment variables from the .env file
load_dotenv()

# Gemini model
MODEL_NAME = "gemini-3.8-flash"


# 1. Define the shared workflow state
class WorkflowState(TypedDict):
    question: str
    documents: list[str]
    answer: str
    retry_count: int
    memory: list[str]
    llm_error: str


# 2. Sample knowledge base
KNOWLEDGE_BASE = [
    "Python is a programming language used for automation and data analysis.",
    "LangGraph builds workflows using nodes, edges, and shared state.",
    "Conditional edges allow workflows to choose their next step.",
    "Memory can preserve conversation context between interactions."
]


# 3. Question node
def question_node(state: WorkflowState):
    print("\nQuestion received:", state["question"])
    return {}


# 4. Retriever node
def retriever_node(state: WorkflowState):
    question = state["question"].lower()

    # Simple keyword-based retrieval
    keywords = [
        word.strip(".,?!")
        for word in question.split()
        if len(word.strip(".,?!")) > 3
    ]

    documents = [
        document
        for document in KNOWLEDGE_BASE
        if any(word in document.lower() for word in keywords)
    ]

    attempt = state["retry_count"] + 1

    print(f"Retriever attempt: {attempt}")
    print("Documents found:", len(documents))

    return {
        "documents": documents,
        "retry_count": attempt
    }


# 5. Real LLM node using Google Gemini
def llm_node(state: WorkflowState):
    documents = state["documents"]

    # Do not call Gemini when retrieval fails
    if not documents:
        return {
            "answer": (
                "I could not find relevant information. "
                "Please try a more specific question."
            ),
            "llm_error": ""
        }

    api_key = os.getenv("GEMINI_API_KEY")

    # Handle missing API key
    if not api_key:
        error_message = (
            "GEMINI_API_KEY was not found. "
            "Check that your .env file exists and is configured."
        )

        print("\nConfiguration error:", error_message)

        return {
            "answer": (
                "Answer generation failed because the Gemini "
                "API key is not configured."
            ),
            "llm_error": error_message
        }

    try:
        client = genai.Client(api_key=api_key)

        context = "\n".join(
            f"- {document}" for document in documents
        )

        prompt = f"""
You are a helpful question-answering assistant.

Answer the user's question in clear, beginner-friendly language.
Use the retrieved context as the source of information.
Do not invent facts that are not supported by the context.
If the context does not contain enough information, say so.

Retrieved context:
{context}

User question:
{state["question"]}
"""

        response = client.interactions.create(
            model=MODEL_NAME,
            input=prompt
        )

        answer = response.output_text

        # Handle an empty response
        if not answer or not answer.strip():
            raise ValueError("Gemini returned an empty response.")

        answer = answer.strip()

        print("\nGemini-generated answer:", answer)

        return {
            "answer": answer,
            "llm_error": ""
        }

    except Exception as error:
        error_message = f"{type(error).__name__}: {error}"

        print("\nGemini request failed:", error_message)

        return {
            "answer": (
                "Sorry, I could not generate an answer right now. "
                "Please check the API key, internet connection, "
                "model availability, and API quota, then try again."
            ),
            "llm_error": error_message
        }


# 6. Memory node
def memory_node(state: WorkflowState):
    updated_memory = state["memory"] + [
        f"Question: {state['question']}",
        f"Answer: {state['answer']}"
    ]

    return {"memory": updated_memory}


# 7. Conditional routing after retrieval
def route_after_retrieval(state: WorkflowState):
    if state["documents"]:
        return "generate_answer"

    if state["retry_count"] < 2:
        print("No documents found. Retrying retrieval...")
        return "retry_retrieval"

    print("Retry limit reached. Using fallback answer.")
    return "generate_answer"


# 8. Build the LangGraph workflow
builder = StateGraph(WorkflowState)

builder.add_node("question", question_node)
builder.add_node("retrieve", retriever_node)
builder.add_node("generate_answer", llm_node)
builder.add_node("memory", memory_node)

builder.add_edge(START, "question")
builder.add_edge("question", "retrieve")

builder.add_conditional_edges(
    "retrieve",
    route_after_retrieval,
    {
        "generate_answer": "generate_answer",
        "retry_retrieval": "retrieve"
    }
)

builder.add_edge("generate_answer", "memory")
builder.add_edge("memory", END)

graph = builder.compile()


# 9. Run the workflow
if __name__ == "__main__":
    question = input("Enter your question: ").strip()

    if not question:
        print("Please enter a non-empty question.")

    else:
        initial_state: WorkflowState = {
            "question": question,
            "documents": [],
            "answer": "",
            "retry_count": 0,
            "memory": [],
            "llm_error": ""
        }

        try:
            result = graph.invoke(initial_state)

            print("\n--- Final Result ---")
            print(result["answer"])

            print("\nConversation memory:")
            print(result["memory"])

            if result["llm_error"]:
                print("\nLLM error details:")
                print(result["llm_error"])

        except Exception as error:
            print(
                "\nWorkflow failed unexpectedly:",
                type(error).__name__,
                str(error)
            )
