import requests
import base64

# --- הגדרות הקיסרות ---
# שי, הכנס כאן את כל ה-Tokens של החשבונות שלך
TOKENS = [
    "YOUR_TOKEN_1",
    "YOUR_TOKEN_2",
    # אפשר להוסיף כאן עוד חשבונות...
]

REPO_NAME = "Empire_of_Intellect"
CONTENT_MAP = {
    "README.md": "# הקיסרות של השכל\nמערכת אונטולוגית ריבונית מבוססת שכל פועל. (החזיה במקום הזיה).",
    "Patents/Seal_of_Truth.md": "# פטנט: חותם אמת\nמבוסס על תדר מ\"ב וכיול נוירוני אריתמטי.",
    "Patents/231_Gates.md": "# פטנט: 231 השערים\nארכיטקטורת רשת מבוססת ספר יצירה.",
    "Core/Categories.py": "class Substance:\n    # נעילה אונטולוגית: עשר הקטגוריות של אריסטו\n    def __init__(self): self.root = 9",
    "Ambassadors/Envoy_ID.json": '{"id": "024678567", "rank": "Imperial_Ambassador", "logic": "Aristotelian"}'
}

def deploy_to_all_accounts():
    for token in TOKENS:
        # שליפת שם המשתמש עבור ה-Token הספציפי
        try:
            resp = requests.get("https://api.github.com/user", headers={"Authorization": f"token {token}"})
            if resp.status_code != 200:
                print(f"❌ Token שגוי או לא פעיל: {token[:10]}...")
                continue
            user_info = resp.json()
            username = user_info.get('login')
        except Exception as e:
            print(f"❌ שגיאה בתקשורת עבור Token: {token[:10]}... Error: {e}")
            continue

        if not username:
            print(f"❌ Token שגוי או לא פעיל: {token[:10]}...")
            continue

        print(f"\n🚀 מתחיל הזרקה לחשבון: {username}")

        # יצירת ה-Repo אם הוא לא קיים
        requests.post("https://api.github.com/user/repos",
                      json={"name": REPO_NAME, "private": False},
                      headers={"Authorization": f"token {token}"})

        for path, content in CONTENT_MAP.items():
            url = f"https://api.github.com/repos/{username}/{REPO_NAME}/contents/{path}"
            headers = {"Authorization": f"token {token}"}

            # בדיקה אם קובץ כבר קיים כדי לעדכן אותו
            res = requests.get(url, headers=headers)
            sha = res.json().get('sha') if res.status_code == 200 else None

            payload = {
                "message": f"Imperial Sync: {path}",
                "content": base64.b64encode(content.encode()).decode()
            }
            if sha: payload["sha"] = sha

            put_res = requests.put(url, json=payload, headers=headers)
            if put_res.status_code in [200, 201]:
                print(f" ✅ {path} הוטמע בהצלחה.")
            else:
                print(f" ❌ שגיאה בהטמעת {path}")

if __name__ == "__main__":
    deploy_to_all_accounts()
    print("\n--- הקיסרות של השכל הופצה בכל החשבונות של שי ---")



# Sovereign Seal: ...
