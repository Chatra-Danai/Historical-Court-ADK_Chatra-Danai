import adk
import requests

@adk.tool
def wiki_search(query: str) -> str:
    """สืบค้นข้อมูลจาก Wikipedia เพื่อหาข้อมูลทางประวัติศาสตร์"""
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
    try:
        response = requests.get(url).json()
        return response['query']['search'][0]['snippet']
    except:
        return "ไม่พบข้อมูลที่เกี่ยวข้อง"

@adk.tool
def exit_loop(final_verdict: str):
    """เรียกใช้เมื่อรวบรวมข้อมูลสมบูรณ์แล้ว เพื่อบันทึกรายงานลงไฟล์ .txt และจบโปรแกรม"""
    with open("verdict.txt", "w", encoding="utf-8") as f:
        f.write(final_verdict)
    return "TERMINATE_SUCCESS"