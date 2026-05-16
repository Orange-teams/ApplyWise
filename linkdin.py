import json
import time
import requests
from bs4 import BeautifulSoup


def fetch_filtered_linkedin_jobs(
    keywords,
    location="Germany",
    job_format="full-time",  # Options: 'full-time' or 'part-time'
    experience_level="entry",  # Options: 'entry' or 'senior'
    max_jobs=5,
    filename="filtered_linkedin_jobs.json",
) -> list:

    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    favorite_jobs = []

    # Map user-friendly text filters to LinkedIn's query parameters
    format_map = {"full-time": "F", "part-time": "P"}
    level_map = {"entry": "2", "senior": "4"}

    # Fallback to default full-time/entry if user types an invalid string
    api_job_format = format_map.get(job_format.lower(), "F")
    api_exp_level = level_map.get(experience_level.lower(), "2")

    print(f"Searching LinkedIn ({location})...")
    print(f"Filters applied -> Format: {job_format}, Level: {experience_level}\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for keyword in keywords:
        if len(favorite_jobs) >= max_jobs:
            break

        print(f"Scanning keyword: '{keyword}'")

        params = {
            "keywords": keyword,
            "location": location,
            "f_JT": api_job_format,  # Job Type Filter Flag
            "f_E": api_exp_level,  # Experience Level Filter Flag
            "start": 0,
        }

        try:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code != 200:
                print(
                    f"    Rate-limited or blocked by LinkedIn (Status {response.status_code})"
                )
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("li")

            for card in job_cards:
                if len(favorite_jobs) >= max_jobs:
                    break

                title_element = card.find(
                    "h3", class_="base-search-card__title"
                )
                company_element = card.find(
                    "h4", class_="base-search-card__subtitle"
                )
                link_element = card.find("a", class_="base-card__full-link")

                # --- NEW: Extract specific exact location from the card element ---
                location_element = card.find(
                    "span", class_="job-search-card__location"
                )

                if title_element and company_element and link_element:
                    job_title = title_element.text.strip()
                    company_name = company_element.text.strip()
                    job_url = link_element["href"].split("?")[0]

                    # Parse out the dynamic localized string (e.g., "Munich, Bavaria, Germany")
                    exact_location = (
                        location_element.text.strip()
                        if location_element
                        else location
                    )

                    # Title Match Validation
                    if keyword.lower() in job_title.lower():
                        job_data = {
                            "title": job_title,
                            "company": company_name,
                            "location": exact_location,  # Added exact localized position to JSON
                            "job_format": job_format.capitalize(),  # Added format field tracking
                            "experience_level": experience_level.capitalize(),  # Added level field tracking
                            "url": job_url,
                            "matched_keyword": keyword,
                        }

                        favorite_jobs.append(job_data)
                        print(
                            f"   Match Found: {job_title} in {exact_location}"
                        )

            time.sleep(3)  # Anti-blocking mechanism delay

        except Exception as e:
            print(f"An error occurred while scanning '{keyword}': {e}")

    # Write dictionary items out cleanly to target file
    if favorite_jobs:
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(favorite_jobs, json_file, indent=4, ensure_ascii=False)
        print(
            f"\n Complete! Saved {len(favorite_jobs)} filtered entries to '{filename}'"
        )
    else:
        print("\n No matching entries found for this strict query setup.")

    return favorite_jobs


# --- ADJUST FILTERS AND RUN ---
if __name__ == "__main__":
    my_keywords = ["Python Developer", "Data Analyst", "Software Engineer"]

    fetch_filtered_linkedin_jobs(
        keywords=my_keywords,
        location="Germany",
        job_format="full-time",  # Options: 'full-time', 'part-time'
        experience_level="entry",  # Options: 'entry', 'senior'
        max_jobs=20,
        filename="linkedin_germany_filtered.json",
    )