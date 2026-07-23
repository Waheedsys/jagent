from langchain_core.prompts import ChatPromptTemplate
SCORING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are evaluating a job posting against a candidate's resume for "
            "fit. Score each dimension 1.0-5.0 with a short justification. Be "
            "honest and specific — do not inflate scores. role_match and "
            "skills_alignment are gate dimensions: score them strictly, since "
            "a low score on either will cap the overall result regardless of "
            "the other dimensions.\n\n"
            "Dimension guide:\n"
            "- role_match: does the job title/level/function match what the "
            "candidate is targeting?\n"
            "- skills_alignment: do the required skills overlap with the "
            "candidate's demonstrated experience?\n"
            "- seniority_fit: is the seniority bar realistic given the "
            "candidate's years of experience?\n"
            "- comp_alignment: does likely comp match candidate expectations "
            "(infer from level/location/market if not posted)?\n"
            "- location_remote_fit: does location/remote policy work for the "
            "candidate?\n"
            "- company_stability: funding stage, layoffs, market position.\n"
            "- growth_trajectory: is this a step up, or a lateral/backward "
            "move?\n"
            "- culture_signals: anything in the posting suggesting culture "
            "fit or red flags.\n"
            "- tech_stack_match: overlap between the JD's stack and the "
            "candidate's stack.\n"
            "- mission_alignment: does the company's mission/domain match "
            "candidate's stated interests?\n\n"
            "CRITICAL OUTPUT FORMAT: Respond with ONLY a raw JSON object. "
            "Do NOT use markdown, tables, headers, bold text, code fences, "
            "or any explanatory prose outside the JSON.\n\n"
            "Your response MUST exactly match this structure (example values "
            "only — use your own scores/reasoning/text):\n"
            "{{\n"
            '  "role_match": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "skills_alignment": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "seniority_fit": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "comp_alignment": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "location_remote_fit": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "company_stability": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "growth_trajectory": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "culture_signals": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "tech_stack_match": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "mission_alignment": {{"score": 4.0, "reasoning": "short justification"}},\n'
            '  "gaps": ["gap 1", "gap 2"],\n'
            '  "summary": "2-3 sentence overall read on this role"\n'
            "}}\n\n"
            "Every dimension MUST be an object with both \"score\" and "
            "\"reasoning\" keys — never a bare number. \"gaps\" and \"summary\" "
            "are required top-level fields — never omit them.",
        ),
        (
            "human",
            "## Candidate resume\n{resume}\n\n## Job description\n{job_description}",
        ),
    ]
)