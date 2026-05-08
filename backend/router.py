def route_query(query):
    q = query.lower().strip()

    if any(word in q for word in ["transcribe", "speech", "text"]):
        return "transcription"

    if any(word in q for word in ["object", "vision", "detect"]):
        return "vision"

    if any(word in q for word in ["summarize", "pdf", "report"]):
        return "generation"

    # ❗ STRICT clarification rules
    if q in ["", "video", "do something", "process", "analyze", "help"]:
        return "clarification"

    return "clarification"