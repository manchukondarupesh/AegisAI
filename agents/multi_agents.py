from drone_db_agent import (
    get_drones,
    get_low_battery_drones,
    get_high_temperature_drones,
    get_failed_missions,
    get_high_alerts,
    get_drone_telemetry
)

from drone_risk_tool import predict_drone_risk
from rag_tool import search_company_documents


def database_agent(question):
    question = question.lower()

    if "low battery" in question:
        return get_low_battery_drones()

    elif "temperature" in question or "hot" in question:
        return get_high_temperature_drones()

    elif (
        "failed mission" in question
        or "failed missions" in question
        or "missions failed" in question
    ):
        return get_failed_missions()

    elif "alert" in question:
        return get_high_alerts()

    else:
        return get_drones()


def supervisor(question):
    question_lower = question.lower()

    # -------------------------
    # ML AGENT
    # -------------------------
    # -------------------------
    # ML AGENT
    # -------------------------
    ml_keywords = [
        "predict",
        "prediction",
        "forecast",
        "risk"
    ]

    if any(word in question_lower for word in ml_keywords):

        # Detect drone ID from the question
        drone_id = None

        for possible_id in ["D-01", "D-02", "D-03", "D-04", "D-05"]:
            if possible_id.lower() in question_lower:
                drone_id = possible_id
                break

        # If no drone ID is mentioned, use D-03
        if drone_id is None:
            drone_id = "D-03"

        telemetry = get_drone_telemetry(drone_id)

        if telemetry is None:
            return {
                "agent": "ML Agent",
                "answer": f"No telemetry data found for {drone_id}."
            }

        battery, temperature, signal_strength = telemetry

        result = predict_drone_risk.invoke({
            "battery": battery,
            "temperature": temperature,
            "signal_strength": signal_strength
        })

        return {
            "agent": "ML Agent",
            "answer": f"Drone: {drone_id}\n{result}"
        }

    # -------------------------
    # RAG AGENT
    # -------------------------
    rag_keywords = [
        "manual",
        "document",
        "policy",
        "procedure",
        "safety",
        "what should",
        "how should",
        "what to do",
        "how to handle",
        "what happens when"
    ]

    if any(word in question_lower for word in rag_keywords):

        result = search_company_documents.invoke({
            "question": question
        })

        return {
            "agent": "RAG Agent",
            "answer": result
        }

    # -------------------------
    # DATABASE AGENT
    # -------------------------
    database_keywords = [
        "drone",
        "battery",
        "temperature",
        "mission",
        "alert",
        "telemetry",
        "status"
    ]

    if any(word in question_lower for word in database_keywords):

        result = database_agent(question)

        return {
            "agent": "Drone Database Agent",
            "answer": result
        }

    # -------------------------
    # DEFAULT SUPERVISOR
    # -------------------------
    return {
        "agent": "Supervisor",
        "answer": "I could not determine the appropriate specialist agent."
    }


if __name__ == "__main__":

    test_questions = [
        "What is the status of the drones?",
        "Which drone has low battery?",
        "Which drone has high temperature?",
        "Which missions failed?",
        "Show high severity alerts",
        "What is the drone safety procedure?",
        "What should happen when a drone has critically low battery?",
        "Predict drone failure risk"
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("QUESTION:", question)

        response = supervisor(question)

        print("SELECTED AGENT:", response["agent"])
        print("ANSWER:", response["answer"])