def get_requirement_weight(requirement):
    """
    Assign an importance level and numerical weight
    to a job requirement.

    Critical  = 3
    Important = 2
    Standard  = 1
    """

    requirement_lower = requirement.lower()

    critical_keywords = [
        "python",
        "generative ai",
        "llm",
        "rag",
        "retrieval-augmented generation",
        "prompt engineering",
        "embeddings",
        "vector database",
        "vector databases",
        "langchain",
    ]

    important_keywords = [
        "sql",
        "cloud",
        "azure",
        "aws",
        "google cloud",
        "docker",
        "kubernetes",
        "ci/cd",
        "mlops",
        "llmops",
        "api",
        "data engineering",
        "data pipelines",
        "responsible ai",
        "security",
        "governance",
    ]

    for keyword in critical_keywords:
        if keyword in requirement_lower:
            return "Critical", 3

    for keyword in important_keywords:
        if keyword in requirement_lower:
            return "Important", 2

    return "Standard", 1


def calculate_weighted_match_score(requirement_analysis):
    """
    Calculate a weighted resume-to-job-description match score.

    Status scoring:
        matched = 1.0
        partial = 0.5
        missing = 0.0
    """

    if not requirement_analysis:
        return {
            "score": 0,
            "matched": 0,
            "partial": 0,
            "missing": 0,
            "total": 0,
            "earned_points": 0,
            "total_possible_points": 0,
            "requirement_scores": []
        }

    matched = 0
    partial = 0
    missing = 0

    earned_points = 0
    total_possible_points = 0

    # Store the scoring details for every requirement
    requirement_scores = []

    for item in requirement_analysis:

        importance, weight = get_requirement_weight(
            item.requirement
        )

        total_possible_points += weight

        if item.status == "matched":
            matched += 1
            earned_points += weight

        elif item.status == "partial":
            partial += 1
            earned_points += weight * 0.5

        elif item.status == "missing":
            missing += 1

        requirement_scores.append({
            "requirement": item.requirement,
            "status": item.status,
            "importance": importance,
            "weight": weight
        })

    score = (earned_points / total_possible_points) * 100

    return {
        "score": round(score, 1),
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "total": matched + partial + missing,
        "earned_points": round(earned_points, 1),
        "total_possible_points": total_possible_points,
        "requirement_scores": requirement_scores
    }