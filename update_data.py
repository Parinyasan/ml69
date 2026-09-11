import os
import json
from github import Github
from github import Auth  # เพิ่มบรรทัดนี้เข้ามา

token = os.environ.get("GH_TOKEN")

# เปลี่ยนวิธี Login ตามที่ PyGithub แนะนำ
auth = Auth.Token(token)
g = Github(auth=auth)

# ⚠️ อาจารย์อย่าลืมเปลี่ยนชื่อ Org ด้านล่างให้ตรงกับของนักศึกษาจริงนะครับ
target_orgs = ["company-a-org", "company-b-org"] 

dashboard_data = {}

for org_name in target_orgs:
    try:
        org = g.get_organization(org_name)
        company_members = {}

        for repo in org.get_repos():
            try:
                contributors = repo.get_contributors()
                for c in contributors:
                    if not c.login: continue 
                    
                    if c.login not in company_members:
                        company_members[c.login] = {
                            "username": c.login,
                            "avatar": c.avatar_url,
                            "commits": 0,
                            "company": org_name
                        }
                    company_members[c.login]["commits"] += c.contributions
            except Exception as e:
                print(f"Skipping repo {repo.name}: {e}")
        
        dashboard_data[org_name] = list(company_members.values())
        print(f"Fetched data for {org_name}")
        
    except Exception as e:
        print(f"Error fetching org {org_name}: {e}")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=4)

print("Data updated successfully!")
