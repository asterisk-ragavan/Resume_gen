import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

JSON_FORMAT = """{
    "personal_info": {
        "name": "Sakthi Ragavan",
        "title": "Software developer | Python Django | DSA | ECE VTU University",
        "email": "sakthiragavan359@gmail.com",
        "phone": "9110421913",
        "location": "Bengaluru, Karnataka, India",
        "linkedin": "https://www.linkedin.com/in/sakthi-ragavan/",
        "linkedin_username": "sakthi-ragavan",
        "github": "https://github.com/asterisk-ragavan",
        "github_username": "asterisk-ragavan"
    },
    "work_experience": [
        {
            "company": "TATA Consultancy Services",
            "title": "Software Developer",
            "start_date": "Jan 2024",
            "end_date": "Present",
            "bullets": [
                "Developed scalable REST APIs using Django and built lightweight web applications with Flask.",
                "Optimized application performance through efficient data structures and algorithms in Python.",
                "Led development activities and supported L2/L3 teams in resolving complex technical issues.",
                "Implemented JWT token-based authentication for API endpoints in the application.",
                "Identified and resolved bugs, contributing to improved system reliability and performance",
                "Expanding expertise in machine learning and AWS cloud computing for scalable solutions."
            ]
        }
    ],
    "education": [
        {
            "institution": "Visvesvaraya Technological University",
            "degree": "B.E Electronics and Communication",
            "gpa": "7.01",
            "start_date": "Aug 2019",
            "end_date": "July 2023",
            "bullets": [
                "Served as Student Club Coordinator, YCOI President, and TCS SPOC, leading various initiatives.",
                "Possess strong presentation skills, effectively delivering engaging and informative project presentations."
            ]
        }
    ],
    "projects": [
        {
            "name": "Role-Based Library Management System",
            "date": "Aug 2022",
            "bullets": [
                "Developed and deployed a Library Management System using Django and MySQL on AWS EC2.",
                "Designed an interactive front-end with Tailwind CSS, Jinja2, Bootstrap, and jQuery.",
                "Implemented role-based access control for students, librarians, and management.",
                "Integrated a weighted ranking system for popular books and export/import functionality in multiple formats."
            ]
        }
    ],
    "skills": [
        {
            "category": "Programming Languages",
            "skills": ["Python", "Java", "C program", "C#"]
        },
        {
            "category": "Frameworks",
            "skills": ["Django", "Flask", "TensorFlow", "Numpy", "Pandas", "ASP.Net", "Selenium", "Rest framework", "MySQL"]
        },
        {
            "category": "Tools",
            "skills": ["AWS", "Microsoft Power Automate", "Blue Prism", "MS Azure", "Docker", "Mainframe", "Github", "Jira"]
        }
    ],
   "certificates": [
        {
            "name": "AWS certified cloud architect",
            "link": "https://www.certificate.udemy.com",
            "about": "about the certificate"
        }
    ],

    "achievements": [
          "Served as Student Club Coordinator, YCOI President, and TCS SPOC, leading various initiatives.",
          "Possess strong presentation skills, effectively delivering engaging and informative project presentations."
    ]
}
"""

def generate_content_from_gemini(html_filepath, resume_filepath, mime_type):
    """
    Generates a tailored resume JSON from Gemini API using the Job Description and current Resume.

    Uses Gemini 2.5 Pro to analyze both documents simultaneously and produce an
    ATS-optimized resume structure.

    Args:
        html_filepath: Path to the HTML file containing the Job Description.
        resume_filepath: Path to the resume file (HTML or PDF).
        mime_type: MIME type of the resume ('text/html' or 'application/pdf').

    Returns:
        Generated JSON string or None on error.
    """
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        # In production, you might want to raise an error or handle this gracefully
        raise ValueError("The GOOGLE_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)
    
    try:
        print("Starting Gemini 2.5 Pro processing...")

        # Construct the prompt
        prompt = f"""
        You are an expert Resume Writer and ATS (Applicant Tracking System) Optimization Specialist.
        Your goal is to rewrite the provided resume so that it is GUARANTEED to be shortlisted for the job described in the Job Description (JD).

        **Input:**
        1.  **Job Description:** Provided as an HTML file.
        2.  **Current Resume:** Provided as a {mime_type} file.

        **Task:**
        Analyze both documents deeply. Create a new, optimized resume JSON object that strictly follows the structure provided below.

        **Optimization Strategy (Aggressive):**
        1.  **Keywords & Skills:** extract ALL relevant hard and soft skills from the JD. Ensure these exact keywords appear in the "skills", "summary", and "work_experience" sections of the new resume.
        2.  **Role Alignment:** Rewrite the "title" in "personal_info" to match the target role in the JD (e.g., if JD says "Senior Python Engineer", and the candidate is "Software Developer", change it to "Software Developer | Aspiring Senior Python Engineer" or similar to match intent).
        3.  **Experience Tailoring:**
            -   Rewrite bullet points in "work_experience" to mirror the language and requirements of the JD.
            -   Highlight achievements that are most relevant to the JD.
            -   If the JD requires a skill (e.g., "Kubernetes") and the candidate has used it in a project but didn't list it explicitly in that role, **add it** to the bullet points if it is truthful to infer based on the context.
            -   Use strong action verbs and quantify results (e.g., "Improved latency by 20%").
            -   **CRITICAL:** Add HTML `<b>` tags around key terms in the bullet points that match the JD requirements. Example: "Developed <b>REST APIs</b> using <b>Django</b>..."
        4.  **Summary:** Write a compelling professional summary that explicitly connects the candidate's background to the company and role. Mention the company name.
        5.  **Gap Filling:** If the JD requires something the candidate *likely* has based on other skills (e.g., JD wants "Git" and candidate has "GitHub"), ensure it is explicitly listed.
        6.  **Format:** The output MUST be a valid JSON object matching the `JSON_FORMAT` schema below. Do NOT add markdown formatting like ```json ... ```. Just the raw JSON string.

        **Output JSON Structure:**
        {JSON_FORMAT}

        **Constraints:**
        -   Do NOT invent false experience. Only emphasize and reframe existing experience.
        -   Keep the JSON structure exact.
        -   Ensure "bullets" fields are arrays of strings.

        Generate the optimized JSON now.
        """

        # Prepare the content parts
        contents = [
            types.Part.from_bytes(
                data=html_filepath.read_bytes(),
                mime_type='text/html',
            ),
            types.Part.from_bytes(
                data=resume_filepath.read_bytes(),
                mime_type=mime_type,
            ),
            prompt
        ]

        # Call the model
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=contents
        )
        
        print("Gemini 2.5 processing completed.")
        # Clean up the response if it contains markdown
        response_text = response.text.strip()
        response_text = response_text.removeprefix('```json').removesuffix('```').strip()

        return response_text

    except Exception as e:
        print(f"Error calling Gemini API (model: gemini-2.5-pro): {type(e).__name__}: {e}")
        # Fallback or re-raise depending on requirements. For now, returning None as per original contract.
        return None
