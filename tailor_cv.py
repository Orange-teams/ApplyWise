import os
import subprocess
import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

# 1. Initialize the Gemini Client
# The SDK automatically pulls the GEMINI_API_KEY environment variable
client = genai.Client()

def get_job_description(url: str) -> str:
    """Scrapes raw text from the job description URL."""
    print(f"Fetching job description from: {url}...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Strip scripts, styles, and footers to keep text clean
        for element in soup(["script", "style", "footer", "nav"]):
            element.decompose()
            
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"Error scraping URL: {e}")
        return ""

def load_master_resume(filepath: str) -> str:
    """Loads your base LaTeX code."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def tailor_resume_with_gemini(master_tex: str, job_desc: str) -> str:
    """Sends the data to Gemini to get tailored LaTeX code back."""
    print("Analyzing and tailoring with Gemini...")
    
    system_instruction = (
        "You are an expert ATS (Applicant Tracking System) optimization agent and an advanced LaTeX engineer. "
        "Your job is to rewrite a candidate's LaTeX resume to align perfectly with a provided job description.\n\n"
        "CRITICAL RULES:\n"
        "1. You MUST return ONLY valid, raw LaTeX code. Do not wrap it in markdown code blocks like ```latex ... "
        "```. Start directly with the LaTeX commands.\n"
        "2. Do not invent fake metrics, companies, or degrees. Tailor the existing experience points using the STAR method, focusing on keywords from the job description.\n"
        "3. Keep all LaTeX formatting, macros, packages, and custom stylings identical. Ensure you escape special characters properly (e.g., use \\& instead of &, and \\% instead of %)."
    )

    prompt = f"""
    Here is my master resume in LaTeX format:
    -----------------------------------------
    {master_tex}
    -----------------------------------------

    Here is the job description I want to target:
    -----------------------------------------
    {job_desc}
    -----------------------------------------

    Please return the updated, fully tailored LaTeX code.
    """

    # We use gemini-2.5-flash as it is lightning fast and excellent at structured text transformations
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2, # Low temperature keeps it precise and factual
        )
    )
    
    return response.text

def compile_pdf(tex_filepath: str, output_filename: str):
    """Compiles the generated .tex file into a PDF using pdflatex."""
    print(f"Compiling {tex_filepath} to PDF...")
    try:
        # Run pdflatex. Interaction=nonstopmode ensures it won't stall on minor warnings
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', f'-jobname={output_filename}', tex_filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Success! Generated {output_filename}.pdf")
            # Optional: Clean up LaTeX auxiliary clutter files
            for ext in ['.log', '.aux', '.out']:
                aux_file = f"{output_filename}{ext}"
                if os.path.exists(aux_file):
                    os.remove(aux_file)
        else:
            print("LaTeX compilation failed. Check the logs below.")
            print(result.stdout[-1000:]) # Print the last 1000 characters of the log
            
    except FileNotFoundError:
        print("Error: 'pdflatex' command not found. Ensure a LaTeX distribution is installed and in your PATH.")

def main():
    # Configuration
    job_url = input("Enter the Job Description URL: ").strip()
    master_resume_path = "master_resume.tex"
    tailored_tex_path = "tailored_output.tex"
    output_pdf_name = "Tailored_CV"
    
    if not os.path.exists(master_resume_path):
        print(f"Error: Could not find '{master_resume_path}' in the current directory.")
        return

    # Execution flow
    job_description = get_job_description(job_url)
    if not job_description:
        print("Failed to acquire job description. Aborting.")
        return
        
    master_tex = load_master_resume(master_resume_path)
    
    tailored_tex = tailor_resume_with_gemini(master_tex, job_description)
    
    # Write the AI generated text to file
    with open(tailored_tex_path, 'w', encoding='utf-8') as f:
        f.write(tailored_tex)
        
    # Compile directly to PDF
    compile_pdf(tailored_tex_path, output_pdf_name)

if __name__ == "__main__":
    main()