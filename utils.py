import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

JSON_FORMAT = """{
  "name": "Jennifer Jobscan",
  "title": "Product Designer",
  "email": "jennifer@jobscan.co",
  "website": "www.jenniferjobscan.co",
  "phone": "123.456.7890",
  "location": "Seattle, WA, 90823, US",
  "summary": "Creative professional and collaborator with 15+ years experience devoted to product, 10+ as a Product Manager and Lead. In-depth knowledge of manufacturing processes, materials, applications, licensing with external partners and approval standards.",
  "work_experience": [
    {
      "title": "Design Directory Consultant",
      "company": "Fashion Forum",
      "location": "Milan",
      "dates": "Feb 2018 - Present",
      "bullets": [
        "Reviewed design concepts, critiqued, and designed fashion based tier 1 headwear that elevated product and brand expression.",
        "Designed quick-to-market regionalized, premium, and mass product line for subsidiary brands under fashion umbrella.",
        "Set up subsidiary brands under Hat Club with sourcing, and S.O.P.s for product creation and development."
      ]
    },
    {
      "title": "Assistant Manager (Design)",
      "company": "StyleMe Inc",
      "location": "New York, NY",
      "dates": "Aug 2016 - Jan 2018",
      "bullets": [
        "Influenced accounts, vendors, and internal stakeholders to support lifestyle product with trend presentation, selling tools, product curating, and exclusives, while delivering renewed company relevance at trade shows through brand collaborations.",
        "Implemented quick-to-market system to react to trends, allowing for customization, low minimums and faster timelines.",
        "Coordinated with factories ensuring proper execution, pricing, and delivery of prototypes and production samples."
      ]
    }
  ],
  "projects": [
    {
      "title": "User Story Development",
      "dates": "Feb 2017 - Aug 2017",
      "bullets": [
        "Developed detailed user personas through extensive research and user interviews to empathize with target users' needs and behaviors. Utilized insights to create personas that informed design decisions, resulting in user-centric solutions that improved user experience and engagement."
      ]
    }
  ],
  "skills": [
    "Photoshop",
    "Illustration",
    "User Interface",
    "User Experience"
  ],
  "education": [
    {
      "institution": "New York University",
      "dates": "Aug 2010 - Dec 2014",
      "degree": "Bachelor Fine Arts Management"
    }
  ],
  "certifications": [
    {
      "name": "Example Certification 1",
      "issuing_organization": "Example Organization",
      "date": "Jan 2023",
      "expires": false,
      "credential_id": null,
      "credential_url": null
    },
      {
      "name": "Example Certification 2",
      "issuing_organization": "Another Organization",
      "date": "June 2022",
      "expires": true,
       "expiry_date": "June 2024",
      "credential_id": "12345ABC",
      "credential_url": "https://example.com/credential/12345ABC"
    }
  ]
}"""

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
        print("html start")
        prompt = """From the following HTML job description Attached, extract the following information and format it as a single, valid JSON object.  Do not include any introductory text or explanations, only the JSON.  The JSON should include these keys:

                *   `job_title`: The title of the job.
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
        HTML_JOB_DATA=response.text

        prompt = """Analyze the following resume text. Extract the following information, and then generate a concise summary suitable for a resume objective or professional summary section. Be specific and use keywords relevant to job applications:

                1.  **Personal Information:**
                    *   Full Name
                    *   Email Address
                    *   Phone Number
                    *   LinkedIn Profile URL (if present)
                    *   Other relevant URLs (portfolio, GitHub, etc.)

                2.  **Education:** For each educational institution, list:
                    *   Institution Name
                    *   Degree Earned
                    *   Major
                    *   Graduation Date (or expected graduation date)
                    *   GPA (if included and above 3.0)
                    *   Relevant coursework or projects (list as comma-separated keywords)

                3.  **Experience:** For each work experience entry, list:
                    *   Company Name
                    *   Job Title
                    *   Start Date
                    *   End Date (or "Present" if currently employed)
                    *   A list of responsibilities and accomplishments, using action verbs and quantifiable results whenever possible.  Present these as bullet points (but represented as plain text, not HTML).

                4.  **Skills:**  List all skills mentioned, categorized if possible (e.g., "Technical Skills:", "Soft Skills:").

                5. **Awards/certifications**: list of awards or certifications

                6.  **Summary:** Create a concise (3-5 sentence) professional summary.  This summary should highlight my key skills, experience level, and career goals.  It should be tailored to a general job application in [mention your target industry/field, e.g., "software engineering," "data science," "marketing"].  The summary *must* be suitable for use in the objective/summary section of a resume.

                Resume Text:
                [Paste your resume text here]"""
        response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            types.Part.from_bytes(
                data=resume_filepath.read_bytes(),
                mime_type=mime_type,
            ),
            prompt])
        RESUME_DATA=response.text

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
            Note: give me the final output Json with relevent information to send to a resume template, dont include any explantion addition text to it.
            only the optimized data in the specified output format is required."""
            
        response = client.models.generate_content(
        model="gemini-2.0-pro-exp-02-05", contents=prompt)
        
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