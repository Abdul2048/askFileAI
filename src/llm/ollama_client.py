import ollama
class OllamaLLM:
    """LLM client using Ollama"""
    
    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        self.client = ollama.Client()
    
    def generate(self, prompt: str, context: str = "") -> str:
        """Generate response from LLM"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            response = self.client.generate(
                model=self.model,
                prompt=full_prompt
            )
            
            return response['response']
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")



