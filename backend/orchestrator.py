from agents.vision_agent import VisionAgent

vision_agent = VisionAgent()


def handle_query(query, video_path):
    query_lower = query.lower()

    # Route to Vision Agent
    if "object" in query_lower or "see" in query_lower:
        result = vision_agent.handle(query, video_path)
        if result:
            return result

    return "Sorry, I couldn't understand the query."