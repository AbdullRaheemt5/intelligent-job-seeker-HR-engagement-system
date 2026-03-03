# ai_engine.py

def analyze_jobseeker(resume_text, job_database, last_active_days):

    skills = []
    for skill in ["Python", "Java", "HTML", "CSS", "JavaScript", "React", "Node"]:
        if skill.lower() in resume_text.lower():
            skills.append(skill)

    job_matches = []
    for job in job_database:
        matched = len(set(skills) & set(job["required_skills"]))
        percent = int((matched / len(job["required_skills"])) * 100)

        job_matches.append({
            "job_title": job["job_title"],
            "match_percentage": percent,
            "missing_skills": list(set(job["required_skills"]) - set(skills))
        })

    job_matches.sort(key=lambda x: x["match_percentage"], reverse=True)

    return {
        "resume_analysis": {
            "resume_strength_score": min(90, 40 + len(skills) * 8),
            "top_skills": skills,
            "improvement_suggestions": [
                "Add measurable achievements",
                "Use ATS-friendly keywords",
                "Include real project impact"
            ]
        },
        "job_recommendations": job_matches,
        "skill_gap_analysis": {
            "target_role_used": job_matches[0]["job_title"],
            "skill_gap_percentage": 100 - job_matches[0]["match_percentage"],
            "missing_skills": job_matches[0]["missing_skills"],
            "suggested_learning_roadmap": [
                "Strengthen fundamentals",
                "Build real-world projects",
                "Practice interview questions"
            ]
        },
        "interview_prep": {
            "technical_questions": [
                "Explain React state",
                "Difference between let and var",
                "What is REST API?"
            ],
            "behavioral_questions": [
                "Tell me about yourself",
                "Describe a challenge you solved"
            ]
        },
        "engagement_message": (
            "You have been inactive for a while. Consider updating your resume."
            if last_active_days > 30 else ""
        )
    }