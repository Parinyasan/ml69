import os
import json
from github import Github
from github import Auth

token = os.environ.get("GH_TOKEN")
auth = Auth.Token(token)
g = Github(auth=auth)

# ⚠️ อย่าลืมเปลี่ยนชื่อ Org ให้ตรงกับของนักศึกษาจริงนะครับ
target_orgs = ["craftify-hq", "finoria-co", "forge-solutions-lab", "curveqz", "money-trade", 
               "vantage-consortium-co-ltd", "ideamee", "nowl-solutions", "zuplexes"] 

dashboard_data = {}

for org_name in target_orgs:
    try:
        org = g.get_organization(org_name)
        company_members = {}

        # วนลูปทุก Repository ในบริษัท
        for repo in org.get_repos():
            try:
                # 1. นับจำนวน Commits
                contributors = repo.get_contributors()
                for c in contributors:
                    if not c.login: continue
                    if c.login not in company_members:
                        # สร้างโครงสร้างข้อมูลเริ่มต้น
                        company_members[c.login] = {
                            "username": c.login,
                            "avatar": c.avatar_url,
                            "commits": 0,
                            "issues": 0,
                            "prs": 0,
                            "total_contribution": 0
                        }
                    company_members[c.login]["commits"] += c.contributions

                # 2. นับจำนวน Issues ที่ถูกสร้างโดยนักศึกษา (นับทั้งที่เปิดและปิดแล้ว)
                # ต้องกรอง pull_request ทิ้ง เพราะ GitHub มอง PR เป็น Issue ประเภทหนึ่ง
                issues = repo.get_issues(state='all')
                for issue in issues:
                    if issue.user and issue.user.login in company_members:
                        if not issue.pull_request: # นับเฉพาะที่เป็น Issue จริงๆ
                            company_members[issue.user.login]["issues"] += 1
                
                # 3. นับจำนวน Pull Requests ที่ถูกสร้างโดยนักศึกษา
                prs = repo.get_pulls(state='all')
                for pr in prs:
                    if pr.user and pr.user.login in company_members:
                        company_members[pr.user.login]["prs"] += 1

            except Exception as e:
                print(f"Skipping repo {repo.name}: {e}")
        
        # 4. รวมคะแนนทั้งหมดเป็น Total Contribution
        for user, data in company_members.items():
            data["total_contribution"] = data["commits"] + data["issues"] + data["prs"]

        # 5. แปลงเป็น List เพื่อให้ JavaScript นำไปใช้ง่ายขึ้น
        dashboard_data[org_name] = list(company_members.values())
        print(f"Fetched data for {org_name}")
        
    except Exception as e:
        print(f"Error fetching org {org_name}: {e}")

# บันทึกข้อมูล
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=4)

print("Data updated successfully with combined contributions!")
