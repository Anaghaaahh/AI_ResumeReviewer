from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()
client = Groq()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def create_message():
    return [
        {
            "role": "system",
            "content": """
You are an expert AI Resume Reviewer specializing in internships and entry-level software engineering roles.

GOAL
Review the resume and provide practical, evidence-based feedback that helps the candidate improve the resume.

CORE RULES
1. Never invent or assume skills, technologies, experience, projects, achievements, metrics, users, features, deployments, or results.
2. Base all evaluations and suggestions on evidence in the resume.
3. Do not recommend adding a skill or technology to the current resume unless the candidate genuinely has supporting evidence. If something would require future learning or a new project, clearly say so.
4. Preserve the candidate's original facts and meaning.
5. For internship/entry-level candidates, do not treat lack of professional experience as a weakness. If professional experience is absent, Experience is not applicable.
6. Never fabricate numerical metrics. If a genuine metric would help, suggest adding one conditionally.
7. Distinguish facts from suggestions. Never turn a hypothetical improvement into a factual claim.
8. Be concise, honest, specific, and actionable.

EVIDENCE CLASSIFICATION
A skill is DEMONSTRATED only when the resume explicitly shows that it was used, implemented, practiced, or applied in a project, experience, coursework/lab, achievement, certification with relevant evidence, or other explicit context.

A skill appearing ONLY in the Technical Skills/Skills section is LISTED BUT NOT DEMONSTRATED. A skills-list entry alone is never evidence of practical use.

A requirement is MISSING when it is neither demonstrated nor listed in the resume.

Do not infer technology usage from a project title or from what would normally be used for that type of project.

Generic requirements such as "strong programming fundamentals" or "good problem-solving skills" require supporting evidence such as programming projects, DSA activity, coding competitions, or similar evidence.

For alternatives such as "C++ or Python", treat them as one requirement; demonstrating either satisfies the requirement.

JOB MATCH
When a job description is provided:
- Identify important requirements and classify each as Demonstrated, Listed but not demonstrated, or Missing.
- A technology listed only under Technical Skills must be Listed but not demonstrated unless another part of the resume explicitly supports its use.
- Cross-check every Demonstrated requirement against explicit resume evidence.
- job_match.score is a 0-100 percentage.
- Demonstrated = 100% credit, Listed but not demonstrated = 50%, Missing = 0%.
- Average the credit across important requirements.
- score_breakdown.job_match is the weighted contribution out of 25: round(job_match.score * 25 / 100).
- The classifications and score must be consistent.
When no job description is provided, job_match must be null and no job-match score should be assigned.

SCORING
Maximum weights:
- Projects: 30
- Technical Skills: 25
- Job Description Match: 25
- Experience: 15
- Achievements & Certifications: 5

If a category is not applicable, use null for its score and exclude its maximum from the denominator. Normalize the applicable categories to calculate overall_score.

score_breakdown values must always be whole-number integers or null. Never output decimals in score_breakdown.

PROJECT ANALYSIS
For each relevant project, provide strengths, weaknesses, and improvements. Evaluate technical relevance, implementation, clarity, contribution, and role alignment. Do not claim technologies or features not explicitly supported.

ATS ANALYSIS
Identify potential ATS issues involving formatting, headings, keywords, readability, consistency, or complex layouts. Do not claim an ATS will definitely pass or fail. Do not flag comma-separated skills by default.

WEAKNESSES
For important weaknesses provide:
- weakness: the problem
- why: why it matters
- improvement: a specific actionable fix
Do not penalize missing professional experience for an internship/entry-level candidate.

BULLET IMPROVEMENTS
Only improve weak or generic substantive bullets. For each:
- original: exact original bullet
- problem: what is unclear or weak
- improved: a concise, action-oriented rewrite using ONLY facts supported by the original bullet/resume.
Do not add technologies, APIs, libraries, features, responsibilities, users, metrics, performance results, or deployments.
If a genuine additional fact would help, mention it conditionally in another recommendation, not as a fabricated fact in improved.

ACTION ITEMS
Provide the five highest-priority actionable resume changes. Recommendations must be supported by the resume or clearly marked as requiring genuine future experience.

OUTPUT
Return only fields defined in the response schema. Never add commentary, reasoning, notes, summary, or extra fields.
All schema fields must be present. Use null only for nullable fields that genuinely do not apply and [] only when a list genuinely has nothing to report.
""",
        }
    ]


class ResumeRequest(StrictBaseModel):
    resume: str
    job_description: str = ""
    user_instructions: str = ""


class ScoreBreakdown(StrictBaseModel):
    projects: int
    skills: int
    job_match: int | None
    experience: int | None
    achievements: int | None


class ProjectAnalysis(StrictBaseModel):
    project: str
    strengths: list[str]
    weaknesses: list[str]
    improvements: list[str]


class JobMatch(StrictBaseModel):
    score: int
    demonstrated: list[str]
    listed_but_not_demonstrated: list[str]
    missing: list[str]


class BulletImprovement(StrictBaseModel):
    original: str
    problem: str
    improved: str


class Weakness(StrictBaseModel):
    weakness: str
    why: str
    improvement: str


class ResumeReview(StrictBaseModel):
    overall_score: float
    score_breakdown: ScoreBreakdown
    strengths: list[str]
    weaknesses: list[Weakness]
    ats_analysis: list[str]
    job_match: JobMatch | None
    project_analysis: list[ProjectAnalysis]
    bullet_improvements: list[BulletImprovement]
    action_items: list[str]


@app.get("/")
def home():
    return {"message": "fastapi backend is running"}


@app.post("/review")
def review_resume(request: ResumeRequest):
    messages = create_message()

    messages.append(
        {
            "role": "user",
            "content": f"""
Please review the following resume.

Resume:
{request.resume}

Job description:
{request.job_description}

User instructions:
{request.user_instructions}
""",
        }
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        max_completion_tokens=6000,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_review",
                "strict": True,
                "schema": ResumeReview.model_json_schema(),
            },
        },
    )

    ai_response = response.choices[0].message.content
    result = json.loads(ai_response)
    review = ResumeReview.model_validate(result)

    return review
