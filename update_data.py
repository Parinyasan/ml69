import os
import json
from github import Github

token = os.environ.get("GH_TOKEN")
g = Github(token)

# ⚠️ อาจารย์อย่าลืมเปลี่ยนชื่อ Org ให้ตรงกับของนักศึกษาจริงนะครับ
target_orgs = ["tensorflow", "pytorch"] 

dashboard_data = {}

for org_name in target_orgs:
    try:
        org = g.get_organization(org_name)
        company_members = {}

        # วนลูปทุก Repository ในบริษัท
        for repo in org.get_repos():
            try:
                # ดึงข้อมูลนักศึกษาที่มีส่วนร่วม (Commit) ใน Repo นี้
                contributors = repo.get_contributors()
                for c in contributors:
                    # บางครั้ง User อาจไม่มีชื่อ ให้ข้ามไปก่อน
                    if not c.login: continue 
                    
                    if c.login not in company_members:
                        company_members[c.login] = {
                            "username": c.login,
                            "avatar": c.avatar_url,
                            "commits": 0,
                            "company": org_name
                        }
                    # c.contributions คือจำนวน commit ที่ทำใน Repo นี้
                    company_members[c.login]["commits"] += c.contributions
            except Exception as e:
                print(f"Skipping repo {repo.name}: {e}")
        
        # แปลงข้อมูลในบริษัทนี้เป็น list เพื่อนำไปใช้ต่อ
        dashboard_data[org_name] = list(company_members.values())
        print(f"Fetched data for {org_name}")
        
    except Exception as e:
        print(f"Error fetching org {org_name}: {e}")

# บันทึกข้อมูล
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=4)

print("Data updated successfully!")
