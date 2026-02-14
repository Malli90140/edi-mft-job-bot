import requests, xml.etree.ElementTree as ET

TOKEN = "YOUR_TOKEN"
CHAT_ID = "1268443681"

KEYWORDS=[
"edi",
"electronic data interchange",
"ibm sterling",
"sterling integrator",
"sterling file gateway",
"managed file transfer",
"mft",
"b2b integration"
]

def send(msg):
    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def match(text):
    return any(k in text.lower() for k in KEYWORDS)

def google_jobs():
    queries=[
    "edi jobs india",
    "ibm sterling integrator jobs",
    "managed file transfer engineer",
    "sterling file gateway jobs"
    ]

    jobs=[]

    for q in queries:
        url=f"https://news.google.com/rss/search?q={q.replace(' ','+')}&hl=en-IN&gl=IN&ceid=IN:en"

        try:
            r=requests.get(url,timeout=20)
            root=ET.fromstring(r.content)

            for item in root.findall(".//item"):
                title=item.find("title").text
                link=item.find("link").text

                if match(title):
                    jobs.append(f"🔹 {title}\n{link}")

        except:
            pass

    return list(dict.fromkeys(jobs))

results=google_jobs()

if results:
    send("🎯 Latest EDI/MFT Jobs\n\n"+"\n\n".join(results[:30]))
else:
    send("No jobs found today")
