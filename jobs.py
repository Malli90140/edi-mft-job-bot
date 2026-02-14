import requests
import xml.etree.ElementTree as ET

TOKEN = "7946541419:AAHziIBBLAd3LBnfBzawpr3lYGC8nr5Rq5U"
CHAT_ID = "1268443681"

KEYWORDS = [
    "edi",
    "electronic data interchange",
    "ibm sterling",
    "sterling integrator",
    "sterling file gateway",
    "managed file transfer",
    "mft",
    "b2b integration",
]

def send(msg):
    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def match(text):
    return any(k in text.lower() for k in KEYWORDS)

def indeed_jobs():
    feeds=[
    "https://in.indeed.com/rss?q=EDI",
    "https://in.indeed.com/rss?q=IBM+Sterling+Integrator",
    "https://in.indeed.com/rss?q=Managed+File+Transfer",
    "https://in.indeed.com/rss?q=Sterling+File+Gateway"
    ]

    jobs=[]

    for url in feeds:
        try:
            r=requests.get(url,timeout=20,headers={"User-Agent":"Mozilla/5.0"})
            root=ET.fromstring(r.content)

            for item in root.findall(".//item"):
                title=item.find("title").text
                link=item.find("link").text

                if match(title):
                    jobs.append(f"🔹 {title}\n{link}")

        except:
            pass

    return list(dict.fromkeys(jobs))

results=indeed_jobs()

if results:
    send("🎯 Latest EDI/MFT Jobs (Indeed)\n\n"+"\n\n".join(results[:30]))
else:
    send("No EDI/MFT jobs found today")
