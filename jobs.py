import requests
from datetime import datetime

TOKEN = "7946541419:AAHziIBBLAd3LBnfBzawpr3lYGC8nr5Rq5U"
CHAT_ID = "1268443681"

KEYWORDS = [
    "EDI","IBM Sterling","Sterling Integrator","B2B Integrator",
    "MFT","Managed File Transfer","Axway","GoAnywhere",
    "Globalscape","Boomi","SAP IDOC","EDIFACT","X12"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def get_jobs():
    url = "https://remotive.com/api/remote-jobs"
    data = requests.get(url).json()

    results=[]
    for job in data["jobs"]:
        text = (job["title"]+" "+job["company_name"]).lower()
        if any(k.lower() in text for k in KEYWORDS):
            results.append(f"{job['title']} - {job['company_name']}\n{job['url']}")

    return results

jobs=get_jobs()

if jobs:
    message="📊 Daily EDI & MFT Jobs\n\n"+"\n\n".join(jobs[:15])
else:
    message="No new EDI/MFT jobs today"

send_telegram(message)
