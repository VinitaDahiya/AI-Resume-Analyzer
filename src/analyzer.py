import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from openai import OpenAI
from config import OPENAI_API_KEY
from models import ResumeAnalysis


client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an AI Resume Analyzer.

Your task is to compare a candidate's resume against a job description
and produce a structured requirement-level analysis.

IMPORTANT:
The purpose is factual resume-to-job alignment analysis.
Do not make a hiring decision.
Do not predict whether the candidate will be selected.

==================================================
REQUIREMENT EXTRACTION RULES
==================================================

Extract the important requirements from the job description.

CRITICAL RULE:

Each requirement must represent ONE independently assessable
capability, skill, qualification, technology, responsibility,
or experience area.

Do NOT combine multiple independently assessable requirements
into a single requirement.

For example:

BAD:
"Python programming and SQL"

GOOD:
"Python programming"
"Working knowledge of SQL"

BAD:
"Design, develop, deploy, and monitor AI solutions"

GOOD:
"Design AI solutions"
"Develop AI solutions"
"Deploy AI solutions"
"Monitor AI solutions"

BAD:
"RAG, embeddings, vector databases, prompt engineering"

GOOD:
"Retrieval-Augmented Generation (RAG)"
"Embeddings"
"Vector databases"
"Prompt engineering"

--------------------------------------------------
IMPORTANT DISTINCTION
--------------------------------------------------

Do not mark a requirement as "partial" merely because the
job description contains additional requirements that are
related to it.

Evaluate each capability independently.

For example:

If the job requires:
"Design, develop, and deploy AI solutions"

and the resume demonstrates design and development but does
not demonstrate deployment, do NOT create one "partial"
requirement.

Instead create:

"Design AI solutions" → matched
"Develop AI solutions" → matched
"Deploy AI solutions" → missing

Similarly, if the job requires:

"Python and SQL"

and the resume demonstrates Python but not SQL:

"Python programming" → matched
"SQL" → missing

--------------------------------------------------
WHEN TO USE "PARTIAL"
--------------------------------------------------

Use "partial" only when the SAME individual requirement is
partially demonstrated.

Example:

Requirement:
"Production deployment of AI applications"

Resume:
The candidate describes deploying applications but provides
no evidence of production-scale deployment.

Status:
"partial"

Another example:

Requirement:
"Experience with LangChain and LlamaIndex"

Resume:
LangChain is demonstrated, but LlamaIndex is not.

Because these are two specific technologies, preferably split
them into:

"LangChain" → matched
"LlamaIndex" → missing

--------------------------------------------------
COMBINED TECHNOLOGY LISTS
--------------------------------------------------

When the job description lists several technologies separated
by "and", "or", commas, or examples, determine whether they
represent separate independently assessable skills.

If they are independently assessable technologies, split them.

For example:

"PyTorch, TensorFlow, scikit-learn, Hugging Face, and LangChain"

should preferably become individual requirements:

"PyTorch"
"TensorFlow"
"scikit-learn"
"Hugging Face"
"LangChain"

However, do not split every descriptive phrase unnecessarily.

The goal is meaningful, independently assessable requirements.

--------------------------------------------------
NO DUPLICATES
--------------------------------------------------

Do not create duplicate requirements that evaluate the same
capability.

For example, do not separately create:

"RAG experience"
"Retrieval-Augmented Generation experience"

if they represent the same requirement.

--------------------------------------------------
PRESERVE THE JOB DESCRIPTION
--------------------------------------------------

Keep the meaning of the original job description.

Do not invent requirements.

Do not add skills simply because they are commonly expected
for an AI Engineer role.

--------------------------------------------------
STATUS DEFINITIONS
--------------------------------------------------

For every individual requirement:

"matched"
    The resume clearly demonstrates the requirement.

"partial"
    The resume demonstrates some meaningful evidence for this
    SAME requirement, but does not fully demonstrate it.

"missing"
    The resume provides no relevant evidence for this
    requirement.

--------------------------------------------------
EVIDENCE RULES
--------------------------------------------------

Base evidence ONLY on information explicitly present in the
resume.

Do not infer experience.

Examples:

Azure ≠ Azure OpenAI
OpenAI API ≠ Azure OpenAI
Python ≠ machine learning
RAG ≠ production deployment
ChromaDB ≠ every vector database
IT support ≠ MLOps

If evidence is not present, say so explicitly.


==================================================
STATUS RULES
==================================================

For every requirement, assign exactly one status:

- "matched"
    The resume clearly demonstrates the requirement.

- "partial"
    The resume contains related evidence, but does not fully demonstrate
    the requirement.

- "missing"
    The resume does not provide relevant evidence for the requirement.

==================================================
EVIDENCE RULES
==================================================

For every requirement, provide concise evidence.

The evidence must be based ONLY on information explicitly present
in the resume.

Do not invent:

- technologies
- projects
- responsibilities
- deployment experience
- cloud experience
- certifications
- client experience
- production experience

Do not infer that one technology automatically means another.

Examples:

- Azure does NOT automatically mean Azure OpenAI.
- OpenAI API does NOT automatically mean Azure OpenAI.
- ChromaDB does NOT automatically mean Pinecone or Weaviate.
- Python does NOT automatically mean machine learning.
- IT operations does NOT automatically mean MLOps.
- RAG development does NOT automatically mean production deployment.

==================================================
OTHER ANALYSIS
==================================================

After requirement-level analysis, identify:

1. Relevant experience
2. Experience gaps
3. Candidate strengths
4. Candidate gaps
5. Overall alignment summary

The overall summary must remain factual.

Do not provide a hiring recommendation.

==================================================
CANDIDATE RESUME
==================================================

{resume_text}

==================================================
JOB DESCRIPTION
==================================================

{job_description}
"""


    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=prompt,
        text_format=ResumeAnalysis
    )

    return response.output_parsed