import os
import json
from github import Github

# 1. อ่าน Token จาก Environment Variable ที่ GitHub Actions ส่งมาให้
token = os.environ.get("GH_TOKEN")
g = Github(token)

# 2. กำหนดรายชื่อ Organization (บริษัท) ของนักศึกษา
target_orgs = ["tensorflow", "pytorch"] # เปลี่ยนเป็นชื่อ Org จริง

dashboard_data = {}

# 3. ดึงข้อมูล (ตัวอย่างการนับจำนวน Repo และ Member)
for org_name in target_orgs:
    try:
        org = g.get_organization(org_name)
        repos = org.get_repos()
        
        # เก็บโครงสร้างข้อมูลเบื้องต้น
        dashboard_data[org_name] = {
            "total_repos": repos.totalCount,
            "latest_activity": "N/A" # สามารถเขียนลอจิกดึง Commit ล่าสุดเพิ่มได้
        }
    except Exception as e:
        print(f"Error fetching {org_name}: {e}")

# 4. บันทึกผลลัพธ์เป็นไฟล์ data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=4)

print("Data updated successfully!")