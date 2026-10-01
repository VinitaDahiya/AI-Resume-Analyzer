
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from scorer import calculate_weighted_match_score
from resume_parser import extract_text_from_pdf
from job_description import read_job_description
from analyzer import analyze_resume


# File paths
resume_path = "./data/sample_resume.pdf"
jd_path = "./data/sample_job_description.docx"


# Extract resume text
resume_text = extract_text_from_pdf(resume_path)

# Extract job description text
job_description = read_job_description(jd_path)


# Analyze resume against job description
analysis = analyze_resume(resume_text,job_description)

score_result = calculate_weighted_match_score(analysis.requirement_analysis)


# Display result
print("\n" + "=" * 80)
print("AI RESUME ANALYSIS")
print("=" * 80)

print("\nRequirement Analysis:")
print("-" * 80)

for item in analysis.requirement_analysis:
    print(f"\nRequirement: {item.requirement}")
    print(f"Status:      {item.status}")
    print(f"Evidence:    {item.evidence}")


print("\n" + "=" * 80)
print("RELEVANT EXPERIENCE")
print("=" * 80)

for item in analysis.relevant_experience:
    print(f"- {item}")


print("\n" + "=" * 80)
print("EXPERIENCE GAPS")
print("=" * 80)

for item in analysis.experience_gaps:
    print(f"- {item}")


print("\n" + "=" * 80)
print("STRENGTHS")
print("=" * 80)

for item in analysis.strengths:
    print(f"- {item}")


print("\n" + "=" * 80)
print("GAPS")
print("=" * 80)

for item in analysis.gaps:
    print(f"- {item}")


print("\n" + "=" * 80)
print("OVERALL ASSESSMENT")
print("=" * 80)

print(analysis.overall_assessment)

print("\n" + "=" * 80)
print("WEIGHTED MATCH SCORE")
print("=" * 80)

print(f"\nMatched requirements : {score_result['matched']}")
print(f"Partial requirements : {score_result['partial']}")
print(f"Missing requirements : {score_result['missing']}")
print(f"Total requirements   : {score_result['total']}")


print(f"\nEarned points        : {score_result['earned_points']}")
print(f"Maximum points       : {score_result['total_possible_points']}")

print(f"\nWeighted Match Score : {score_result['score']}%")






print("\n" + "=" * 80)
print("REQUIREMENT WEIGHTS")
print("=" * 80)

for item in score_result["requirement_scores"]:
    print(
        f"\nRequirement : {item['requirement']}"
        f"\nStatus      : {item['status']}"
        f"\nImportance  : {item['importance']}"
        f"\nWeight      : {item['weight']}"
    )