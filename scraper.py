import requests
import json
import re
from datetime import datetime

print(r"""
    ██▓ ███▄    █   ██████ ▄▄▄█████▓ ▄▄▄       ██▀███   ▄▄▄       ███▄ ▄███▓
   ▓██▒ ██ ▀█   █ ▒██    ▒ ▓  ██▒ ▓▒▒████▄    ▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒
   ▒██▒▓██  ▀█ ██▒░ ▓██▄   ▒ ▓██░ ▒░▒██  ▀█▄  ▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░
   ░██░▓██▒  ▐▌██▒  ▒   ██▒░ ▓██▓ ░ ░██▄▄▄▄██ ▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ 
   ░██░▒██░   ▓██░▒██████▒▒  ▒██▒ ░  ▓█   ▓██▒░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒
   ░▓  ░ ▒░   ▒ ▒ ▒ ▓▒▒ ░░▒  ▒ ░░    ▒▒   ▓▒█░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░
    ▒ ░░ ░░   ░ ▒░░ ░░ ░░  ▒ ░       ▒   ▒▒ ░  ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░
    ▒ ░   ░   ░ ░   ░  ░    ░         ░   ▒     ░░   ░   ░   ▒   ░      ░   
    ░           ░         ░               ░  ░   ░           ░  ░       ░   
                                                                           
     ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  ▓█████  ██▀███  
   ▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
   ░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
     ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄ 
   ▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░░▒████▒░██▓ ▒██▒
   ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░
   ░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░      ░ ░  ░  ░▒ ░ ▒░
   ░  ░  ░  ░          ░░   ░   ░   ▒   ░░          ░     ░░   ░ 
         ░  ░ ░         ░           ░  ░            ░  ░   ░     
            ░                                                       
""")
print("=" * 70)
print("instagram scraper by axom".center(70))
print("=" * 70)
print()

username = input("enter instagram username (without @): ").strip()
if not username:
    print("error: empty username")
    exit()

url = f"https://www.instagram.com/{username}/"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

try:
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        print(f"error: profile not found or private (http {r.status_code})")
        exit()
except Exception as e:
    print(f"request error: {e}")
    exit()

html = r.text
match = re.search(r'window\._sharedData\s*=\s*({.*?});', html)
if not match:
    match = re.search(r'<script type="application/json" data-sjs>([^<]+)</script>', html)
    if not match:
        print("error: cannot extract page data")
        exit()
    rawjson = match.group(1)
else:
    rawjson = match.group(1)

try:
    data = json.loads(rawjson)
except:
    print("error: json parse failed")
    exit()

prof = data.get("entry_data", {}).get("ProfilePage", [])
if not prof:
    print("error: no profile data")
    exit()

user = prof[0].get("graphql", {}).get("user", {})
if not user:
    print("error: user missing")
    exit()

fullname = user.get("full_name", "n/a")
bio = user.get("biography", "n/a")
exturl = user.get("external_url", "n/a")
private = user.get("is_private", False)
verified = user.get("is_verified", False)
bcat = user.get("business_category_name", "n/a")
bemail = user.get("business_email", "n/a")
bphone = user.get("business_phone_number", "n/a")
followers = user.get("edge_followed_by", {}).get("count", 0)
following = user.get("edge_follow", {}).get("count", 0)
postcount = user.get("edge_owner_to_timeline_media", {}).get("count", 0)
picurl = user.get("profile_pic_url_hd", user.get("profile_pic_url", "n/a"))
atype = "business" if bcat != "n/a" else "personal"

posts = []
edges = user.get("edge_owner_to_timeline_media", {}).get("edges", [])
for e in edges:
    node = e.get("node", {})
    caption = ""
    capnodes = node.get("edge_media_to_caption", {}).get("edges", [])
    if capnodes:
        caption = capnodes[0].get("node", {}).get("text", "")
    posts.append({
        "code": node.get("shortcode", ""),
        "caption": caption[:500],
        "likes": node.get("edge_media_preview_like", {}).get("count", 0),
        "comments": node.get("edge_media_to_comment", {}).get("count", 0),
        "time": datetime.fromtimestamp(node.get("taken_at_timestamp", 0)).isoformat(),
        "url": node.get("display_url", "")
    })

print("\n" + "=" * 70)
print(f"instagram profile: @{username}".center(70))
print("=" * 70)
print()
print(f"full name: {fullname}")
print(f"bio: {bio}")
print(f"external url: {exturl}")
print(f"private account: {private}")
print(f"verified: {verified}")
print(f"business category: {bcat}")
print(f"business email: {bemail}")
print(f"business phone: {bphone}")
print(f"account type: {atype}")
print(f"profile picture url: {picurl}")
print()
print(f"posts count: {postcount}")
print(f"followers count: {followers}")
print(f"following count: {following}")
print()
print("recent posts (first 12)")
print("-" * 40)
for i, p in enumerate(posts[:12], 1):
    print(f"{i}. https://instagram.com/p/{p['code']}")
    print(f"   likes: {p['likes']} | comments: {p['comments']}")
    print(f"   timestamp: {p['time']}")
    if p['caption']:
        capshort = p['caption'][:150]
        if len(p['caption']) > 150:
            capshort += "..."
        print(f"   caption: {capshort}")
    else:
        print("   caption: none")
    print()
print(f"scraped at: {datetime.now().isoformat()}")
print("=" * 70)
