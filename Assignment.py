import adk
import os
import requests

# 1. นิยาม Tools (ต้องประกาศก่อนสร้าง Agent)
@adk.tool
def wiki_search(query: str) -> str:
    """สืบค้น Wikipedia เพื่อหาข้อมูลประวัติศาสตร์"""
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    res = requests.get(url).json()
    return str(res['query']['search'][0]['snippet']) if res['query']['search'] else "No data"

@adk.tool
def exit_loop(final_verdict: str):
    """บันทึกไฟล์และจบการทำงาน (โจทย์บังคับใช้ Tool นี้)"""
    with open("verdict.txt", "w", encoding="utf-8") as f:
        f.write(final_verdict)
    print("--- บันทึกไฟล์ verdict.txt เรียบร้อยแล้ว! ---")
    return "TERMINATE_SUCCESS"

# 2. นิยาม Agents
admirer = adk.Agent(
    name="admirer",
    instruction="หาด้านบวกของ {subject?}. บันทึกใน 'pos_data'",
    tools=[wiki_search],
    output_key="pos_data"
)
critic = adk.Agent(
    name="critic",
    instruction="หาด้านลบของ {subject?}. บันทึกใน 'neg_data'",
    tools=[wiki_search],
    output_key="neg_data"
)
judge = adk.Agent(
    name="judge",
    instruction="ตรวจสมดุล {pos_data?} และ {neg_data?}. ถ้าสมบูรณ์ให้เรียก 'exit_loop' เท่านั้น",
    tools=[exit_loop]
)

# 3. สร้าง Workflow ตาม Lab GENAI106
investigation = adk.Parallel(branches=[admirer, critic])
trial_loop = adk.Loop(
    node=judge,
    exit_condition=lambda state: "TERMINATE_SUCCESS" in str(state.get("judge_output", ""))
)
court_system = adk.Sequential(steps=[investigation, trial_loop])

# 4. ส่วนสำคัญสำหรับการรัน
if __name__ == "__main__":
    # ใส่ API Key ของคุณที่นี่ (ห้ามเว้นว่าง)
    os.environ["GOOGLE_API_KEY"] = "ใส่_API_KEY_ของคุณที่นี่"
    
    print("--- เริ่มการพิจารณาคดีประวัติศาสตร์ ---")
    court_system.run({"subject": "Genghis Khan"})
    print("--- รันเสร็จสิ้น ---")