<head>
main():json.jn
    print("Hello from GEMA5 -Hello from Anatolii Savchenko__ == "__main__":
    main()
 LLM GEMA-google-gemini/gemini-cli}
class GEMAGenerator(LLMInterface):
    def generate(self, prompt: str, mode: str) -> Tuple[str, Union[None, str], float]:
        if "CRITIQUE_NEEDED" in prompt:
            return "Re-generated code based on critique.", "result = 2 * (25 + 30)", 0.85 
        if mode == "MATH":
            return "Initial draft solution is X. Code: result = (2 * (50 + 3)) / 2", "result = 2 * (50 + 3) / 2", 0.70
        return f"Draft answer for {mode} task.", None, 0.90Critic 
class GEMACritic(LLMInterface):
    def generate(self, prompt: str, mode: str) -> Tuple[str, Union[None, str], float]:
        """Генерує критику та протокол виправлення."""
        if "CRITIQUE_PROTOCOL" in prompt:
            return "CRITIQUE: The previous code did not account for integer truncation. FIX: Use floating point division and re-run. CRITIQUE_NEEDED", None, 0.98
        return "Not a critique query.", None, 0.0
class GEMA_FusionAgent_5_0:
    def __init__(self, threshold: float = 0.80):
        self.generator = GEMAGenerator("GEMA-Gen")
        self.critic = GEMACritic("GEMA-Crit")
        self.encoder = ViTRBMEncoder()
        self.sandbox = OfflineCodeSandbox()
        self.retriever = KnowledgeRetriever()
        self.verifier = DualVerifier(self.sandbox)
        self.confidence_threshold = threshold
    def solve(self, input_data: Union[str, np.ndarray], mode: str) -> dict:
        GEMA 5.0 (Council Agent).
        RBM/ViT -> RAG -> Generator -> [CS Check] -> Critic/Reflection.
        Fusion (ViT/RBM):
        input_vector = self.encoder.encode(input_data)
        
        RAG & Knowledge Retrieval
        knowledge_snippets, verif_templates = self.retriever.retrieve(str(input_data)[:50], mode)
        
        Generation (Generator LLM)
        prompt = f"TASK: {input_data}. MODE: {mode}. VECTOR: {input_vector}. KNOWLEDGE: {knowledge_snippets}."
        draft_solution, code_to_exec, confidence_score = self.generator.generate(prompt, mode)
        attempts = 0
        while confidence_score < self.confidence_threshold and attempts < 2:
            Verification (Sandbox + RAG-Triggered)
            is_verified, result_or_error = self.verifier.verify(code_to_exec, verif_templates)
            
            if is_verified:
                draft_solution = draft_solution.replace("result = 2 * (50 + 3) / 2", str(result_or_error))
                confidence_score = 0.99
                break
            Reflection (Critic LLM) - 
            critique_prompt = f"CRITIQUE PROTOCOL. DRAFT: {draft_solution}. ERROR: {result_or_error}. REVIEW."
            critique, _, _ = self.critic.generate(critique_prompt, mode)
            Regeneration Generator LLM
            regenerate_prompt = f"CRITIQUE_NEEDED. {prompt} CRITIQUE_FROM_CRITIC: {critique}."
            draft_solution, code_to_exec, confidence_score = self.generator.generate(regenerate_prompt, mode)
        attempts += 1
        if code_to_exec:
            _, final_result = self.verifier.verify(code_to_exec, verif_templates)
            final_solution = f"{draft_solution} FINAL RESULT: {final_result}"
        else:
            final_solution = draft_solution
            
        return {
            "solution": final_solution,
            "confidence_score": confidence_score,
            "verification_status": "Verified" if confidence_score > self.confidence_threshold else "Unverified/Draft",
            "image_mask": True i mode == "DIAGNOSTICS"
if __name__ Anatolii Savchenko '__main__':
    agent = GEMA_FusionAgent_5_0(threshold=0.85)
     CS)
    math_problem = "Find the roots of 3x^2 + 5x + 1 = 0. [EQUATION]"
    print("\n--- Сценарій 1: MATH (Council Logic) ---")
    result_math = agent.solve(math_problem, "MATH")
    print(json.dumps(result_math, indent=4)
    mock_image_input = np.random.rand(256, 256, 3)
    
    print("\n--- Сценарій 2: DIAGNOSTICS (ViT/RBM Fusion) ---")
    result_diag = agent.solve(mock_image_input, "DIAGNOSTICS")
    print(json.dumps(result_diag, indent=4))
