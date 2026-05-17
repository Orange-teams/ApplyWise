import os
import re
import json
import time

# Import the scraping function from linkdin.py
from linkdin import fetch_filtered_linkedin_jobs

# Import the tailoring, downloading, and compiling functions from tailor_cv copy
# Note: Since 'tailor_cv copy.py' has a space in its filename, you should rename it 
# to 'tailor_cv.py' so Python can import it cleanly.
from tailor_cv import get_job_description, tailor_resume_with_gemini, compile_pdf

def sanitize_folder_name(name: str) -> str:
    """Sanitizes strings to make them safe for directory names."""
    sanitized = name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    sanitized = re.sub(r'(?u)[^-\w]', '_', sanitized)
    return re.sub(r'_+', '_', sanitized).strip('_')

def main():
    # 1. Configuration
    master_resume_path = "main.tex"
    output_base_dir = "applications"
    #my_keywords = ["Python Developer", "Data Analyst", "Software Engineer"]
    my_keywords = ["Applied scientist", "Data scientist", "AI Engineer"]
    
    if not os.path.exists(master_resume_path):
        print(f"Error: Could not find '{master_resume_path}' in the current directory.")
        return

    # 2. Step 1: Execute the LinkedIn search from linkdin.py
    print("Step 1: Fetching jobs from LinkedIn...")
    jobs = fetch_filtered_linkedin_jobs(
        keywords=my_keywords,
        location="Germany",
        job_format="full-time",
        experience_level="senior",
        max_jobs=10,
        filename="linkedin_germany_filtered.json",
    )
    
    if not jobs:
        print("No jobs found. Exiting pipeline.")
        return
        
    print(f"\nFound {len(jobs)} jobs. Loading your master CV...")
    
    # Load your master latex structure once
    with open(master_resume_path, 'r', encoding='utf-8') as f:
        master_tex = f.read()

    # 3. Step 2: Loop through positions, create folders, and tailor
    for idx, job in enumerate(jobs, 1):
        title = job.get("title", "Unknown_Title")
        company = job.get("company", "Unknown_Company")
        url = job.get("url")
        
        print(f"\n=================== PROCESSING JOB {idx}/{len(jobs)} ===================")
        print(f"Target: {title} at {company}")
        
        if not url:
            print("Skipping: No URL available for this position.")
            continue
            
        # Create a dedicated, sanitized folder for this application
        folder_name = sanitize_folder_name(f"{company}_{title}")
        job_dir = os.path.join(output_base_dir, folder_name)
        os.makedirs(job_dir, exist_ok=True)
        
        # Scrape job description text using tailor_cv's function
        job_description = get_job_description(url)
        if not job_description:
            print("Skipping: Unable to fetch job description.")
            continue
            
        # Send to Gemini for tailoring
        tailored_tex = tailor_resume_with_gemini(master_tex, job_description)
        
        # Save the raw LaTeX output directly inside the new folder
        tailored_tex_path = os.path.join(job_dir, "tailored_output.tex")
        with open(tailored_tex_path, 'w', encoding='utf-8') as f:
            f.write(tailored_tex)
            
        # Compile the PDF
        # Note: To avoid compilation issues with relative styling assets (.cls / .sty files) 
        # located in your root directory, we use pdflatex's -output-directory flag.
        output_pdf_name = f"CV_{sanitize_folder_name(company)}"
        print(f"Compiling PDF into: {job_dir}")
        
        try:
            import subprocess
            # We call pdflatex here explicitly targeting the created directory so your
            # root directory style definitions remain accessible during compilation
            result = subprocess.run(
                [
                    'pdflatex', 
                    '-interaction=nonstopmode', 
                    f'-output-directory={job_dir}', 
                    f'-jobname={output_pdf_name}', 
                    tailored_tex_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                print(f"Success! Saved {output_pdf_name}.pdf inside '{job_dir}'")
                # Clean up auxiliary logs inside that folder
                for ext in ['.log', '.aux', '.out']:
                    aux_file = os.path.join(job_dir, f"{output_pdf_name}{ext}")
                    if os.path.exists(aux_file):
                        os.remove(aux_file)
            else:
                print("LaTeX compilation failed. Log preview:")
                print(result.stdout[-800:])
                
        except Exception as e:
            print(f"An error occurred during compilation: {e}")
            
        # Anti-throttling delay between processing iterations
        time.sleep(2)

if __name__ == "__main__":
    main()