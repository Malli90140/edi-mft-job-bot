import requests
import xml.etree.ElementTree as ET

TOKEN = "7946541419:AAHziIBBLAd3LBnfBzawpr3lYGC8nr5Rq5U"
CHAT_ID = "1268443681"

KEYWORDS = [
    "sterling integrator",
    "sterling file gateway",
    "ibm sterling",
    "electronic data interchange",
    "edi",
    "managed file transfer",
    "mft",
    "b2b integration",
]

HEADERS={"User-Agent":"Mozilla/5.0"}

def send(msg):
    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def match(text):
    return any(k in text.lower() for k in KEYWORDS)

# ---------- LinkedIn ----------
def linkedin():
    urls=[
    "https://www.linkedin.com/jobs-guest/jobs/rss/?keywords=EDI",
    "https://www.linkedin.com/jobs-guest/jobs/rss/?keywords=IBM%20Sterling%20Integrator",
    "https://www.linkedin.com/jobs-guest/jobs/rss/?keywords=Managed%20File%20Transfer"
    ]
    results=[]
    for url in urls:
        r=requests.get(url,headers=HEADERS)
        root=ET.fromstring(r.content)
        for item in root.findall(".//item"):
            title=item.find("title").text
            link=item.find("link").text
            if match(title):
                results.append(f"🔹 {title}\n{link}")
    return results

# ---------- Naukri ----------
def naukri():
    results=[]
    try:
        url="https://www.naukri.com/jobapi/v3/search?keyword=EDI&noOfResults=20"
        r=requests.get(url,headers=HEADERS).json()
        for job in r.get("jobDetails",[]):
            title=job.get("title","")
            company=job.get("companyName","")
            link="https://www.naukri.com"+job.get("jdURL","")
            if match(title+" "+company):
                results.append(f"🔹 {title} - {company}\n{link}")
    except:
        pass
    return results

# ---------- Hirist ----------
def hirist():
    results=[]
    try:
        url="https://www.hirist.tech/api/v1/search/jobs?q=edi"
        r=requests.get(url,headers=HEADERS).json()
        for job in r.get("jobs",[]):
            title=job.get("title","")
            company=job.get("company_name","")
            link="https://www.hirist.tech"+job.get("url","")
            if match(title+" "+company):
                results.append(f"🔹 {title} - {company}\n{link}")
    except:
        pass
    return results

# ---------- Foundit ----------
def foundit():
    results=[]
    try:
        url="https://www.foundit.in/srp/results?query=EDI"
        r=requests.get(url,headers=HEADERS).text
        # simple detection
        if "EDI" in r:
            results.append("🔹 Foundit has EDI jobs today\nhttps://www.foundit.in")
    except:
        pass
    return results

all_jobs = list(dict.fromkeys(
    linkedin() + naukri() + hirist() + foundit()
))

if all_jobs:
    msg="🔥 Daily EDI/MFT Jobs (All Portals)\n\n"+"\n\n".join(all_jobs[:40])
else:
    msg="No EDI/MFT jobs found today"

send(msg)
