import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# --- 1. SET UP GROQ API KEY ---
os.environ["GROQ_API_KEY"] = "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"

# --- 2. LOAD THE VECTOR DATABASE ---
print("Waking up the AI Audit Assistant...")
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_db = FAISS.load_local(
    "faiss_audit_index", 
    embeddings_model, 
    allow_dangerous_deserialization=True 
)

# Set up the retriever to grab the 3 most relevant chunks
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

# --- 3. INITIALIZE THE LLM ---
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

# --- 4. INTERACTIVE CHAT LOOP ---
print("\n" + "="*50)
print("🤖 AI Audit Assistant is online and ready!")
print("Type 'quit' or 'exit' to stop.")
print("="*50)

while True:
    query = input("\nAsk a question about the audit data: ")
    
    if query.lower() in ['quit', 'exit']:
        print("Shutting down... Goodbye!")
        break
        
    if not query.strip():
        continue
        
    # --- THE BARE-METAL RAG ORCHESTRATION ---
    # Step A: Retrieve the relevant documents from FAISS
    docs = retriever.invoke(query)
    
    # Step B: Stitch the document text together into one giant string
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # Step C: Build the prompt manually, injecting the context and the user's question
    prompt = f"""You are an expert AI Data Assistant for business audits. 
    Use ONLY the following retrieved audit context to answer the user's question. 
    If the answer is not contained in the context, do not guess. Simply state: 'I do not have enough information based on the current audit logs.'
    
    Context:
    {context_text}
    
    User Question: {query}
    
    Answer:"""
    
    # Step D: Send the final prompt to the LLM
    response = llm.invoke(prompt)
    
    print(f"\nAnswer: {response.content}")