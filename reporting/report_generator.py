def generate_report(results):
    return {
        "final_score": results["score"],
        "classification": results["verdict"],
        "details": results["reasons"]
    }
