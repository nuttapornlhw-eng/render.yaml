# Backlink Finder (Flask)

เว็บแอปสำหรับค้นหาและคัดเว็บไซต์ทำ Backlink ตามเงื่อนไข DR/UR/DA/PA และ Spam Score (Moz) พร้อมส่งออก CSV

## คุณสมบัติ
- กรอก **keyword** และ **target URL**
- ค้นหาแหล่งโพสต์ฟรีจาก 3 วิธี:
  1) คีย์เวิร์ดแพทเทิร์น (เช่น “{keyword} + \"write for us\"”)
  2) ลิสต์เริ่มต้น (free-post starter list) ที่ให้มา
  3) (ตัวเลือก) ใช้ SerpAPI (ต้องใส่คีย์)
- ตรวจเช็คค่าจาก **Ahrefs API** (DR/UR) และ **Moz API** (DA/PA & Spam Score) — ต้องใส่คีย์
- กรองเว็บที่มีคุณภาพ และ Spam Score <= 3
- เลือก Top 100 และส่งออก CSV ได้

> หมายเหตุ: ถ้าไม่ได้ใส่คีย์ API ระบบจะทำงานในโหมด Demo (สุ่มค่าจำลองชัดเจน) เพื่อทดสอบ UI/Flow เท่านั้น

## การติดตั้ง (แนะนำ Python 3.10+)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# แก้ค่าในไฟล์ .env ให้ถูกต้อง (ใส่ API keys ถ้ามี)
flask --app app run --debug
```

## ไฟล์สำคัญ
- `app.py` — Flask app
- `utils/ahrefs_client.py` — ฟังก์ชันเรียก Ahrefs API (หรือจำลอง)
- `utils/moz_client.py` — ฟังก์ชันเรียก Moz API (หรือจำลอง)
- `utils/discovery.py` — ค้นหา candidate sites จาก patterns / SerpAPI / starter list
- `data/starter_list.csv` — ลิสต์เว็บโพสต์ฟรีตั้งต้น 120+ domains
- `templates/index.html` — UI หน้าเดียว
- `static/main.js` — ฟังก์ชันฝั่ง client
- `.env.example` — ตัวอย่าง environment config

## Environment (.env)
```
# โหมดจำลอง ถ้าไม่มีคีย์ ให้ตั้ง TRUE
DEMO_MODE=TRUE

# Ahrefs
AHREFS_API_KEY=

# Moz
MOZ_ACCESS_ID=
MOZ_SECRET_KEY=

# SerpAPI (ถ้าจะใช้ค้นหา Google SERP)
SERPAPI_KEY=

# ค่ากรองเริ่มต้น (แก้ได้ใน UI เช่นกัน)
MIN_DR=40
MIN_UR=20
MIN_DA=35
MIN_PA=20
MAX_SPAM_SCORE=3
TOP_N=100
```
