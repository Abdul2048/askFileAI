
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from config import Config
from src.embeddings.ollama_embeddings import OllamaEmbeddings
from src.vectorstore.chroma_store import ChromaVectorStore
from src.llm.ollama_client import OllamaLLM
from src.rag.chunker import TextChunker
from src.agent.state import AgentState
from src.file_loaders.file_loader_factory import FileLoaderFactory

class AskFileAIAgent:
    """LangGraph agent for file Q&A"""
    
    def __init__(self, config: Config):
        self.config = config
        self.embeddings = OllamaEmbeddings(config.EMBEDDING_MODEL)
        self.vector_store = ChromaVectorStore(
            config.CHROMA_DB_DIR,
            config.COLLECTION_NAME
        )
        self.llm = OllamaLLM(config.LLM_MODEL)
        self.chunker = TextChunker(config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        
        
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        
        workflow.add_node("load_file", self._load_file)
        workflow.add_node("chunk_text", self._chunk_text)
        workflow.add_node("embed_chunks", self._embed_chunks)
        workflow.add_node("store_vectors", self._store_vectors)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("generate_answer", self._generate_answer)
        
       
        workflow.set_entry_point("load_file")
        workflow.add_edge("load_file", "chunk_text")
        workflow.add_edge("chunk_text", "embed_chunks")
        workflow.add_edge("embed_chunks", "store_vectors")
        workflow.add_edge("store_vectors", "retrieve")
        workflow.add_edge("retrieve", "generate_answer")
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    def _load_file(self, state: AgentState) -> AgentState:
        """Load file content"""
        try:
            loader = FileLoaderFactory.get_loader(state["file_path"])
            content = loader.load(state["file_path"])
            state["file_content"] = content
            state["error"] = ""
        except Exception as e:
            state["error"] = f"File loading error: {str(e)}"
            state["file_content"] = ""
        return state
    
    def _chunk_text(self, state: AgentState) -> AgentState:
        """Chunk the file content"""
        if state["error"]:
            return state
        
        try:
            metadata = {"source": state["file_path"]}
            chunks = self.chunker.chunk_text(state["file_content"], metadata)
            state["chunks"] = chunks
        except Exception as e:
            state["error"] = f"Chunking error: {str(e)}"
        return state
    
    def _embed_chunks(self, state: AgentState) -> AgentState:
        """Generate embeddings for chunks"""
        if state["error"] or not state["chunks"]:
            return state
        
        try:
            texts = [chunk["text"] for chunk in state["chunks"]]
            embeddings = self.embeddings.embed_documents(texts)
            state["embeddings"] = embeddings
        except Exception as e:
            state["error"] = f"Embedding error: {str(e)}"
        return state
    
    def _store_vectors(self, state: AgentState) -> AgentState:
        """Store vectors in ChromaDB"""
        if state["error"]:
            return state
        
        try:
            self.vector_store.add_documents(state["chunks"], state["embeddings"])
        except Exception as e:
            state["error"] = f"Vector storage error: {str(e)}"
        return state
    
    def _retrieve(self, state: AgentState) -> AgentState:
        """Retrieve relevant documents"""
        if state["error"]:
            return state
        
        try:
            query_embedding = self.embeddings.embed_text(state["question"])
            retrieved = self.vector_store.similarity_search(
                query_embedding,
                k=self.config.TOP_K_RESULTS
            )
            state["retrieved_docs"] = retrieved
        except Exception as e:
            state["error"] = f"Retrieval error: {str(e)}"
        return state
    
    def _generate_answer(self, state: AgentState) -> AgentState:
        """Generate answer using LLM"""
        if state["error"]:
            state["answer"] = f"Error: {state['error']}"
            return state
        
        try:
           
            context = "Retrieved context:\n\n"
            for i, doc in enumerate(state["retrieved_docs"]):
                context += f"[Document {i+1}]\n{doc['text']}\n\n"
            
          
            prompt =  f"""
You are a professional summarizer and information extraction agent.

Your job:
- Read the context
- Understand its meaning
- Produce a clean, structured, high-quality answer
- Avoid repetition
- Combine overlapping chunks intelligently

Rules:
- DO NOT repeat sentences from different chunks.
- If the user asks for a summary, provide a concise bullet-point summary.
- If the user asks a general question, provide a clear, organized response.
- Ignore duplicate or overlapping text.

Context:
{context}

Question: {state['question']}

Now provide the BEST possible answer:
"""
            
            answer = self.llm.generate(prompt)
            state["answer"] = answer
            
           
            if "conversation_history" not in state:
                state["conversation_history"] = []
            state["conversation_history"].append({
                "question": state["question"],
                "answer": answer
            })
            
        except Exception as e:
            state["answer"] = f"Answer generation error: {str(e)}"
        
        return state
    
    def ask(self, file_path: str, question: str) -> Dict[str, Any]:
        """Ask a question about a file"""
        self.vector_store.clear_collection()
        initial_state = {
            "file_path": file_path,
            "question": question,
            "file_content": "",
            "chunks": [],
            "embeddings": [],
            "retrieved_docs": [],
            "answer": "",
            "conversation_history": [],
            "error": ""
        }
        
        result = self.graph.invoke(initial_state)
        return result


