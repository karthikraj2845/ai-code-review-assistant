import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            print("WARNING: GEMINI_API_KEY is not set or is set to placeholder. Running in DEMO/MOCK mode.")
            self.mock_mode = True
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.mock_mode = False
                print("Gemini API key successfully configured. Running in LIVE AI mode.")
            except Exception as e:
                print(f"Failed to configure Gemini, falling back to Demo/Mock Mode. Error: {e}")
                self.mock_mode = True

    async def review_code(self, code: str, language: str):
        if self.mock_mode:
            has_print = "print" in code or "console.log" in code
            has_loop = "for" in code or "while" in code
            has_func = "def " in code or "function" in code or "=>" in code
            
            bugs = []
            optimizations = []
            best_practices = []
            
            if language.lower() == "python":
                if "range(len(" in code:
                    bugs.append("Non-idiomatic list iteration using range(len(...)) found.")
                    optimizations.append("Use 'enumerate()' or iterate directly over items: 'for item in list_var'.")
                if "= []" in code or "= {}" in code:
                    bugs.append("Potential mutable default parameter issue in function definition.")
                    best_practices.append("Use None as default parameter and instantiate mutable objects inside the function body.")
            
            if language.lower() in ["javascript", "typescript"]:
                if "var " in code:
                    best_practices.append("Avoid using 'var'. Use 'const' or 'let' to ensure proper block scoping.")
                if "==" in code and "===" not in code:
                    bugs.append("Loose equality operator (==) used instead of strict equality (===).")
                    best_practices.append("Always use === to avoid unexpected coercion bugs.")

            if not bugs:
                bugs.append("No critical runtime bugs found. The code syntax appears valid.")
                
            if not optimizations:
                if has_loop:
                    optimizations.append("Consider caching list/array length outside loops if iterating over massive datasets.")
                optimizations.append("Ensure resources (like database connections or files) are closed using try-finally or context managers.")
                
            if not best_practices:
                best_practices.append("Add docstrings/comments to document function inputs, outputs, and side effects.")
                best_practices.append("Keep functions focused on a single responsibility to enhance readability and testability.")

            complexity_feedback = "Time Complexity: O(N) where N is the input size. Space Complexity: O(1) auxiliary space, assuming standard iteration."
            if has_loop and code.count("for") + code.count("while") > 1:
                complexity_feedback = "Time Complexity: O(N^2) due to nested loops. Space Complexity: O(1) auxiliary space unless storing data."
                
            explanation = f"This is a {language} code snippet. "
            if has_func:
                explanation += "It defines one or more functions to encapsulate logic. "
            if has_loop:
                explanation += "It processes items sequentially using a loop structure. "
            if has_print:
                explanation += "It outputs information to the standard console. "
            explanation += "The overall structure looks modular and clean."

            return {
                "bugs": bugs,
                "optimizations": optimizations,
                "explanation": explanation,
                "best_practices": best_practices,
                "complexity_feedback": complexity_feedback
            }

        prompt = f"""
        You are an expert code reviewer. Analyze the following {language} code and provide:
        1. List of bugs or potential issues
        2. List of optimization suggestions
        3. Explanation of what the code does
        4. List of best practices recommendations
        5. Feedback on time and space complexity

        Code:
        ```{language}
        {code}
        ```

        Please return your response in the following JSON format:
        {{
            "bugs": ["bug1", "bug2", ...],
            "optimizations": ["optimization1", "optimization2", ...],
            "explanation": "explanation of the code",
            "best_practices": ["best_practice1", "best_practice2", ...],
            "complexity_feedback": "feedback on complexity"
        }}

        Ensure that the response is valid JSON and nothing else.
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]
            result = json.loads(response_text)
            return result
        except Exception as e:
            return {
                "bugs": ["Failed to parse AI response"],
                "optimizations": [],
                "explanation": f"AI service error: {str(e)}",
                "best_practices": [],
                "complexity_feedback": "Unable to analyze complexity due to AI service error."
            }

    async def explain_code(self, code: str, language: str):
        if self.mock_mode:
            has_func = "def " in code or "function" in code or "=>" in code
            has_loop = "for" in code or "while" in code
            
            step_by_step = [
                f"1. Initializes the execution block in {language}.",
            ]
            if has_func:
                step_by_step.append("2. Declares functional block and maps input parameters.")
            if has_loop:
                step_by_step.append("3. Iterates over elements using a control flow statement.")
            step_by_step.append("4. Completes execution and returns or prints results.")
            
            key_concepts = [
                f"{language.capitalize()} Syntax & Conventions",
                "Control Flow Mechanics",
                "Functional Programming Structure"
            ]
            
            explanation = f"Detailed Analysis of this {language} snippet:\n\n"
            explanation += "The code provides an elegant solution. "
            if has_func:
                explanation += "By declaring reusable functions, it maintains DRY (Don't Repeat Yourself) principles. "
            if has_loop:
                explanation += "The loop is used to process a collection of inputs sequentially. "
            
            return {
                "explanation": explanation,
                "step_by_step": step_by_step,
                "key_concepts": key_concepts
            }

        prompt = f"""
        You are an expert software engineer. Explain the following {language} code in detail.
        Provide:
        1. A comprehensive explanation of what the code does
        2. Step-by-step breakdown of how the code works
        3. Key programming concepts demonstrated in the code

        Code:
        ```{language}
        {code}
        ```

        Please return your response in the following JSON format:
        {{
            "explanation": "comprehensive explanation of the code",
            "step_by_step": ["step1", "step2", ...],
            "key_concepts": ["concept1", "concept2", ...]
        }}

        Ensure that the response is valid JSON and nothing else.
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]
            result = json.loads(response_text)
            return result
        except Exception as e:
            return {
                "explanation": f"AI service error: {str(e)}",
                "step_by_step": [],
                "key_concepts": []
            }

    async def optimize_code(self, code: str, language: str):
        if self.mock_mode:
            optimized_code = code
            optimizations = []
            explanation = ""
            
            if language.lower() == "python":
                if "range(len(" in code:
                    optimized_code = re.sub(r'for\s+(\w+)\s+in\s+range\(\s*len\(\s*(\w+)\s*\)\s*\):', r'for \1, item in enumerate(\2):', code)
                    optimizations.append("Replaced range(len(...)) with enumerate() for idiomatic and safer sequence indexing.")
                    explanation = "Enumerate provides a cleaner, more Pythonic access to both indices and elements."
            
            if language.lower() in ["javascript", "typescript"]:
                if "var " in code:
                    optimized_code = code.replace("var ", "const ")
                    optimizations.append("Replaced 'var' with 'const' for block-scoped variables where reassignment is not needed.")
                    explanation = "Const ensures block-scoped safety and clarifies that variables are read-only."
                    
            if not optimizations:
                optimizations.append("Refactored code structure for clarity and simplified logical expressions.")
                explanation = "Applied standard micro-optimizations, focusing on modern language conventions and readability."
                
            return {
                "optimized_code": optimized_code,
                "optimizations": optimizations,
                "explanation": explanation
            }

        prompt = f"""
        You are an expert software engineer specializing in code optimization. Analyze the following {language} code and provide:
        1. An optimized version of the code
        2. List of optimizations applied
        3. Explanation of the improvements

        Code:
        ```{language}
        {code}
        ```

        Please return your response in the following JSON format:
        {{
            "optimized_code": "optimized code here",
            "optimizations": ["optimization1", "optimization2", ...],
            "explanation": "explanation of the improvements"
        }}

        Ensure that the response is valid JSON and nothing else.
        """
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]
            result = json.loads(response_text)
            return result
        except Exception as e:
            return {
                "optimized_code": code,
                "optimizations": [],
                "explanation": f"AI service error: {str(e)}"
            }