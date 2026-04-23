import os
from datetime import datetime


def generate_report(results):
    
    # Create reports directory
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Safe subject for filename
    safe_subject = results["subject"].replace(" ", "_").replace("/", "")[:30]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"reports/{safe_subject}_{results["email_id"]}_{timestamp}.txt" 

    with open(filename, "w", encoding='utf-8') as f:
        f.write("\n" + "="*60 + "\n")
        f.write(f"📌 Subject : {results['subject']}\n")
        f.write(f"📊 Score   : {results['score']}\n")
        f.write(f"🚨 Verdict : {results['verdict']}\n")

        f.write("\n🔍 Module Breakdown:\n")
        for k, v in results["breakdown"].items():
            f.write(f"  {k.upper():15} : {v}\n")

        f.write("\n⚠️ Reasons:\n")
        if results["reasons"]:
            for r in results["reasons"]:
                f.write(f"  - {r}\n")
        else:
            f.write("  No suspicious indicators.\n")

        f.write("="*60 + "\n")
    return filename