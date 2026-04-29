class ReRanker:
    """LLM-based semantic re-ranking"""

    def __init__(self, llm_client):
        self.llm = llm_client

    def rerank(self, question: str, retrieved_docs: list, top_k: int = 3):
        scored_docs = []

        for doc in retrieved_docs:
            text = doc["text"][:500]  # limit length for efficiency

            prompt = (
                f"Question: {question}\n"
                f"Content: {text}\n\n"
                "Rate how relevant this content is to the question on a scale from 0 to 1. "
                "Only output the number."
            )

            try:
                score_str = self.llm.generate(prompt)
                score = float(score_str.strip())
            except:
                score = 0.0

            doc["rerank_score"] = score
            scored_docs.append(doc)

        # Sort by score descending
        scored_docs.sort(key=lambda x: x["rerank_score"], reverse=True)

        return scored_docs[:top_k]
