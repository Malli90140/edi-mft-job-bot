import requests

TOKEN = "7946541419:AAHziIBBLAd3LBnfBzawpr3lYGC8nr5Rq5U"
CHAT_ID = "1268443681"

# MUST HAVE (at least one required — core skills)
MANDATORY = [
    "sterling integrator",
    "sterling file gateway",
    "ibm sterling",
    "electronic data interchange",
    "edi",
    "managed file transfer",
    "mft"
]

# GOOD MATCH (extra relevance for your profile)
GOOD = [
    "x12","edifact","idoc",
    "as2","sftp","ftp","oftp",
    "trading partner",
    "b2b integration",
    "integration support",
    "production support",
    "edi analyst",
    "edi support",
    "b2b support",
    "map editor",
    "sterling b2bi",
    "seeburger",
    "opentext",
    "service now",
    "servicenow"
]

# BAD MATCH (reject unrelated jobs)
EXCLUDE = [
    "java developer",
    "full stack",
    "react",
    "angular",
    "sales",
    "marketing",
    "data engineer",
    "ai engineer",
    "frontend",
    "backend developer",
    "ui developer",
    "python developer",
    "machine learning",
    "devops engineer",
    "cloud architect"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def relevant(job):
    text = (
        job["title"] + " " +
        job["company_name"] + " " +
        job.get("description","")
    ).lower()

    # Reject unwanted roles
    if any(b in text for b in EXCLUDE):
        return False

    # Must contain core EDI/MFT skills
    if not any(m in text for m in MANDATORY):
        return False

    # Must also have at least one supporting skill
    score = sum(1 for g in GOOD if g in text)
    return score >= 1

def get_jobs():
    url = "https://remotive.com/api/remote-jobs"
    data = requests.get(url).json()

    results=[]
    for job in data["jobs"]:
        if relevant(job):
            results.append(f"🔹 {job['title']} - {job['company_name']}\n{job['url']}")

    return results

jobs=get_jobs()

if jobs:
    message="🎯 Matching EDI/MFT Jobs For You\n\n"+"\n\n".join(jobs[:20])
else:
    message="No matching Sterling/EDI/MFT jobs today"

send_telegram(message)
