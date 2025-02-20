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
    Generates content from Gemini API using file paths.

    Args:
        html_filepath: Path to the HTML file.
        resume_filepath: Path to the resume file (HTML or PDF).
        mime_type: MIME type of the resume ('text/html' or 'application/pdf').
        prompt: The prompt string.

    Returns:
        Generated text or None on error.
    """
    
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("The GOOGLE_API_KEY environment variable is not set.")
    
    try:
        print("JD processing")
        prompt = """From the following HTML job description Attached, extract the following information and format it as a single, valid JSON object.  Do not include any introductory text or explanations, only the JSON.  The JSON should include these keys:

                *   `job_title`: this format  "Software developer | Python Django | DSA |" note this is according to job discription provided.
                *   `company_name`: The name of the company.
                *   `required_skills`: An array of strings, listing each required skill individually.  Be as granular as possible (e.g., instead of 'programming', list 'Python', 'JavaScript', 'SQL').
                *   `preferred_skills`: An array of strings, similar to `required_skills`.
                *   `years_of_experience`: Extract the minimum years of experience required.  If a range is given, use the lower end.  If no explicit years are mentioned, put 'null'.  Return this as a number (integer or null), not a string.
                *   `education`:  A string describing the required education level (e.g., "Bachelor's Degree in Computer Science", "High School Diploma", "Master's Degree").  If multiple options are acceptable, list them, separated by "or".
                *   `responsibilities`: An array of strings, listing each key responsibility as a separate item. Be concise but complete.
                """
                
        response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            types.Part.from_bytes(
                data=html_filepath.read_bytes(),
                mime_type='text/html',
            ),
            prompt])
        print("JD completed")
        HTML_JOB_DATA=response.text

        print("Resume processing")
        prompt = """
        Analyze the attached resume text and extract the information into structured categories. Then, use the extracted information to generate a concise summary suitable for a resume objective or professional summary section.

        **Instructions:**

        1.  **Data Extraction:** Extract the following information from the resume text, presenting it in the specified format:

            *   **Personal Information:**
                *   Full Name:
                *   Email Address:
                *   Phone Number:
                *   LinkedIn Profile URL: (If present)
                *   Other relevant URLs: (Portfolio, GitHub, etc. - list each with a label)

            *   **Education:** For *each* educational institution, provide:
                *   Institution Name:
                *   Degree Earned:
                *   Major:
                *   Start Date: (Month and Year - e.g., "Aug 2019")
                *   End Date: (Month and Year - e.g., "Aug 2019", or "Present")
                *   GPA: (If included)
                *   Summary of learnings: (Briefly describe the key areas of study or skills acquired)

            *   **Experience:** For *each* work experience entry, provide:
                *   Company Name:
                *   Job Title:
                *   Start Date: (Month and Year - e.g., "Aug 2019")
                *   End Date: (Month and Year - e.g., "Aug 2019", or "Present")
                *   Responsibilities and Accomplishments: (Present as a plain text list of bullet points. Use action verbs at the beginning of each point. Quantify results whenever possible.  Do *not* use HTML.)
                    * Example:
                        *  "Managed a team of 5 developers, increasing project delivery speed by 15%."
                        *  "Developed and implemented a new customer onboarding process, reducing churn by 10%."

            *   **Skills:** List all skills mentioned. Categorize them if possible.  Use clear category labels (e.g., "Technical Skills:", "Soft Skills:", "Tools:", "Programming Languages:").

            * **Awards/Certifications:**
                * List of awards or certifications: (Provide the name of each award or certification)

            * **Achievements:** List Key achievements separately, extracted from various sections of the resume (experience, projects, awards, etc.). Present these as individual, concise bullet points (plain text, not HTML).  Focus on quantifiable results and impactful contributions.

        2.  **Summary Generation:**

            *   Create a concise (3-5 sentence) professional summary suitable for the objective/summary section of a resume.
            *   Target Industry/Field: **[Specify your target industry/field here.  Be precise.  Examples: "Software Engineering (Backend Development)", "Data Science (Machine Learning)", "Digital Marketing (Social Media Strategy)", "Financial Analysis", "Project Management (Construction)"]**
            *   The summary *must* highlight:
                *   Key Skills (select the most relevant 3-5 skills for the target industry)
                *   Experience Level (e.g., "Entry-level", "Experienced professional with X years of experience", "Recent graduate")
                *   Career Goals (briefly and generally, aligning with the target industry)
            * The summary *must* be written in a professional, third-person style.
        """
                
        response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            types.Part.from_bytes(
                data=resume_filepath.read_bytes(),
                mime_type=mime_type,
            ),
            prompt])
        print("Resume processing")
        RESUME_DATA=response.text

        print("Building Resume")
        prompt = f"""I am creating a customized resume using a Jinja2 template.  I have the following inputs:

            1.  **Job Information (JSON):**  This JSON contains details about the job I'm applying for.
            2.  **Resume Information (Text):** This text contains my extracted resume details, including my summary, experience, skills, and education.
            3.  **Output format (JSON):** the final output the prompt should produce

            My goal is to identify the relevant information from my resume that can be altered according to the job requirements and format it for insertion into specific sections of my Jinja2 resume template.

            Here's how the information should be processed and combined:

            *   **Prioritize Matching Skills:** Compare the `required_skills` and `preferred_skills` from the Job Information with the `Skills` section from my Resume Information.  Identify any direct matches and *prioritize* those skills also mention some things whicha re for sure required in my resume accordint to the requirnments.
            *   **Tailor the Summary:** Modify my existing resume summary (from Task 2) to *specifically* mention the company name and job title from the Job Information.  Incorporate 2-3 of the most relevant *required* skills into the summary.
            *   **Highlight Relevant Experience:**  For each entry in my `Experience` section (from Task 2), assess its relevance to the job description.  If the job description mentions specific responsibilities or technologies include them  in my experiance as i did it to increase the chance of selected.  Rewrite the experience points to use keywords from the job description whenever possible.
            *   **Education Matching:** Check if my `Education` meets the `education` requirements in the Job Information.  If the job specifies a particular degree or field of study, ensure that's prominently displayed.
            *   **Quantifiable Results:** Wherever possible, in both the summary and experience sections, use numbers and data to quantify my accomplishments (e.g., "Reduced costs by 15%," "Managed a team of 5 developers").
            *   **Certifications :heiglate the certifications and courses on resume**
            generate the JSON structure of the final optimized resume Data in the output json format.

            **Inputs:**

            *Job Information (JSON):*
            {HTML_JOB_DATA}

            *Resume Information (Text):*
            {RESUME_DATA}
            
            *Output Json Format:
            {JSON_FORMAT}*
            
            Note: 1.  give me the final output Json with relevent information to send to a resume template, dont include any explantion addition text to it.
                  2.  dont include dates if unknown ill use if statement to hide if not found in json.
                  4. add bold tag (HTML tag) the important keywords in the fianl output resule data for the bullet opints, if skills required in jd are present in output bullets add bold tag.
                  3.  only the optimized data in the specified output format is required, you can overwrite things from my resume to make output sutable for the role iam applying. """
            
        response = client.models.generate_content(
        model="gemini-2.0-pro-exp-02-05", contents=prompt)
        print("Resume Built")
        
        return response.text
    
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None
      
# def generate_content_from_gemini_exp(html_filepath, resume_filepath, mime_type):
  
#   client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
  
#   sample_pdf_1 = client.files.upload(
#   file=html_filepath,
#   config=dict(mime_type='text/html')
#   )
#   sample_pdf_2 = client.files.upload(
#     file=resume_filepath,
#     config=dict(mime_type=mime_type)
#   )

#   prompt = f"""I will provide you with two files:

# 1. **Job Description:** An HTML file containing the job description for a specific role.
# 2. **Resume:** A PDF file containing my current resume.

# Your task is to analyze both files and generate a JSON output that can be used with Jinja2 templating to create a tailored resume. This new resume should be aggressively optimized to align with the job requirements and significantly improve the chances of getting shortlisted by Applicant Tracking Systems (ATS) and human recruiters, even if it requires adding information not explicitly present in my original resume (while ensuring it's truthful and plausible).

# **Instructions:**

# 1. **Analyze:** Carefully analyze the job description to identify:
#     * **Keywords:** Extract relevant keywords related to skills, experience, qualifications, and industry terms.
#     * **Requirements:** List the specific requirements mentioned in the job description (e.g., years of experience, specific software proficiency, educational qualifications).
#     * **Responsibilities:** Understand the key responsibilities associated with the role.
#     * **Desired Skills:** Identify both hard and soft skills that are desired for the position.

# 2. **Compare & Enhance:** Compare the job description requirements with my existing resume. Identify:
#     * **Matching Skills/Experience:** Highlight areas where my resume aligns with the job description.
#     * **Missing Skills/Experience:** Identify any skills or experience mentioned in the job description that are missing from my resume.  **Critically, if a skill or experience is required and plausible given my background, add it to the JSON output even if it wasn't explicitly in my original resume.  For example, if the job requires "experience with Agile methodologies" and I have project experience, you can add "Experience with Agile methodologies" to the JSON, even if my resume just mentioned "project management."  The goal is to make my resume as strong as possible while remaining truthful.**  If you need to infer something, add a comment in the JSON like "// Inferred based on project X and job description."
#     * **Areas for Improvement:** Note areas in my resume that could be rephrased or expanded to better highlight relevant qualifications.

# 3. **Generate JSON Output:** Create a JSON object with the following structure:

# ```json output format : {JSON_FORMAT}"""

#   response = client.models.generate_content(
#   model="gemini-2.0-pro-exp-02-05",
#   contents=[sample_pdf_1, sample_pdf_2, prompt])
#   return response.text