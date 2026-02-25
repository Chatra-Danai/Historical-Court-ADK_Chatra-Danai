import adk
import requests
import os

# --- STEP 2: Technical Constraints - Tools Definition ---
@adk.tool
def wiki_search(query: str) -> str:
    """สืบค้นข้อมูลจาก Wikipedia ตาม keyword ที่ระบุ"""
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    try:
        response = requests.get(url).json()
        return str(response['query']['search'][0]['snippet'])
    except:
        return "ไม่พบข้อมูลที่ต้องการ"

@adk.tool
def exit_loop(final_verdict: str):
    """เรียกใช้เมื่อข้อมูลสมบูรณ์แล้ว เพื่อบันทึกผลลง verdict.txt"""
    with open("verdict.txt", "w", encoding="utf-8") as f:
        f.write(final_verdict)
    return "SUCCESS_TERMINATE"

# --- STEP 1 & 2: Agent Definitions & Parallel Logic ---
# Agent A (Admirer)
admirer = adk.Agent(
    instruction="ค้นหาด้านบวกของ {subject?}. ใช้ wiki_search เติมคำว่า 'achievements'",
    tools=[wiki_search]
)

# Agent B (Critic)
critic = adk.Agent(
    instruction="ค้นหาด้านลบของ {subject?}. ใช้ wiki_search เติมคำว่า 'controversy'",
    tools=[wiki_search]
)

# Agent C (Judge)
judge = adk.Agent(
    instruction="ตรวจ {pos_data?} และ {neg_data?}. ถ้าสมบูรณ์แล้วให้เรียก exit_loop",
    tools=[exit_loop]
)

# --- STEP 3: Loop Logic & Architecture ---
investigation = adk.Parallel(
    branches=[admirer, critic],
    outputs={"pos_data": admirer.output, "neg_data": critic.output}
)

trial_loop = adk.Loop(
    node=judge,
    exit_condition=lambda state: "SUCCESS" in str(state.get("judge_output", ""))
)

# Final Workflow
court_system = adk.Sequential(steps=[investigation, trial_loop])

if __name__ == "__main__":
    # ใส่ API Key ของคุณตรงนี้
    os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE" 
    court_system.run({"subject": "Genghis Khan"})