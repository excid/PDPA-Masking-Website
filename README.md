# PDPA Masking Website

เว็บแอปสำหรับปิดบัง (mask) ข้อมูลส่วนบุคคลในข้อความ/log ด้วย **Regular Expression**
ตามแนวคิดของ PDPA — ข้อความที่ส่งเข้ามาไม่ถูกบันทึกลงฐานข้อมูล ประมวลผลในหน่วยความจำแล้วทิ้งทันที

- **Backend**: Django 5 (Python 3.12)
- **Frontend**: HTMX + Alpine.js (ไม่มี build step, ไม่ต้องใช้ Node)
- **Test**: pytest + pytest-django
- **Deploy**: Docker (พร้อมขึ้น Render / Hugging Face Spaces)

> สถานะปัจจุบัน: **skeleton** — โครงสร้างและ orchestrator ทำงานได้จริงแล้ว
> ส่วนกฎ regex ทั้ง 5 ข้อยังเป็น stub (คืนข้อความเดิม) รอเจ้าของกฎมาเขียน

---

## เริ่มต้นใช้งาน

### แบบใช้ Docker (แนะนำ — ทุกคนในทีมได้สภาพแวดล้อมเหมือนกัน)

```bash
cp .env.example .env
docker compose build
docker compose up          # เปิด http://localhost:8000
```

รันเทสต์:

```bash
docker compose run --rm test
# หรือ  make test
```

### แบบ virtualenv ในเครื่อง

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
python manage.py runserver
pytest
```

---

## โครงสร้างโปรเจกต์

```
.
├── config/                     # ตั้งค่า Django (settings แยก dev / prod)
│   ├── settings/{base,dev,prod}.py
│   ├── urls.py  wsgi.py  asgi.py
├── masking/                    # แอปหลัก
│   ├── engine/                 # ★ เอนจิน — Python ล้วน ไม่ผูกกับ Django
│   │   ├── types.py            #   Detection (สัญญากลางของทุกกฎ)
│   │   ├── base.py             #   RegexRule (คลาสฐานที่ทุกคนสืบทอด)
│   │   ├── masker.py           #   orchestrator: รวมผล + จัด overlap + แทนที่
│   │   ├── registry.py         #   ทะเบียนกฎทั้งหมด
│   │   └── rules/              #   ★ หนึ่งไฟล์ = หนึ่งคน (merge แล้วไม่ชนกัน)
│   │       ├── credit_card.py  #     คนที่ 2
│   │       ├── phone.py        #     คนที่ 2
│   │       ├── email.py        #     คนที่ 3
│   │       ├── dob.py          #     คนที่ 4
│   │       └── address.py      #     คนที่ 5
│   ├── api.py                  # JSON API   (คนที่ 7)
│   ├── views.py forms.py       # หน้าเว็บ HTMX (คนที่ 6-7)
│   ├── templates/masking/      # base + index + partials   (คนที่ 6)
│   └── static/masking/         # css / js                  (คนที่ 6)
├── tests/                      # หนึ่งไฟล์ต่อหนึ่งกฎ + orchestrator + api
├── samples/sample_log.txt      # log ตัวอย่างสำหรับเดโม
├── docs/                       # ตารางอธิบาย regex + วิธีทำงานร่วมกัน
├── Dockerfile  docker-compose.yml  Makefile
└── requirements.txt  requirements-dev.txt
```

---

## สถาปัตยกรรม: ทำไมต้องแยก engine ออกจาก Django

`masking/engine/` ไม่ import Django เลยแม้แต่บรรทัดเดียว ผลคือ

1. คนเขียน regex เทสต์งานตัวเองได้โดยไม่ต้องรันเว็บ
2. คนทำ frontend/API ทำงานคู่ขนานได้ทันทีเพราะ stub ใช้งานได้อยู่แล้ว
3. ย้ายเอนจินไปใช้ที่อื่น (CLI, notebook) ได้โดยไม่ต้องแก้อะไร

### สัญญาระหว่างกฎกับเอนจิน

ทุกกฎสืบทอด `RegexRule` แล้วกำหนด 4 อย่าง: `name`, `label`, `pattern`, `mask()`

```python
class EmailRule(RegexRule):
    name = "email"
    label = "อีเมล"
    pattern = re.compile(r"...", re.VERBOSE)

    def mask(self, match: re.Match) -> str:
        ...        # คืน string ที่ mask แล้ว
```

- ถ้า pattern มี named group ชื่อ **`target`** เอนจินจะ mask เฉพาะช่วงของกลุ่มนั้น
  ใช้แทน lookbehind ความยาวไม่คงที่ (ซึ่ง `re` ไม่รองรับ) เช่นคง prefix `DOB:` ไว้
- ใส่ตรรกะที่ regex เขียนแล้วอ่านไม่รู้เรื่องไว้ใน `is_valid()` เช่น เช็ควัน 31/02 หรือ Luhn

### วิธีจัดการช่วงข้อความที่ทับกัน

ห้าม mask ทีละกฎแบบไล่เรียงกัน เพราะข้อความที่ถูก mask แล้วจะโดนกฎถัดไปจับซ้ำ
`masker.py` จึงทำ 3 ขั้น:

| ขั้น | ฟังก์ชัน | ทำอะไร |
|---|---|---|
| 1 | `collect_detections()` | ทุกกฎ scan ข้อความ **ต้นฉบับ** คืน `(start, end)` |
| 2 | `resolve_overlaps()` | ช่วงที่ทับกันเก็บอันที่ยาวกว่า (เลขบัตร 16 หลัก ชนะ เบอร์โทร 10 หลัก) |
| 3 | `apply_detections()` | แทนที่ **จากท้ายไปหน้า** เพื่อไม่ให้ index เพี้ยน |

---

## ตารางกฎ regex

| # | กฎ | `name` | ตัวอย่าง input → output | ผู้รับผิดชอบ | สถานะ |
|---|---|---|---|---|---|
| 1 | บัตรเครดิต | `credit_card` | `4111-1111-1111-1234` → `****-****-****-1234` | คนที่ 2 | stub |
| 2 | เบอร์โทรศัพท์ | `phone` | `081-234-5678` → `***-***-5678` | คนที่ 2 | stub |
| 3 | อีเมล | `email` | `somchai@example.com` → `s*******@example.com` | คนที่ 3 | stub |
| 4 | วันเดือนปีเกิด | `dob` | `DOB: 15/08/2540` → `DOB: **/**/****` | คนที่ 4 | stub |
| 5 | ที่อยู่ | `address` | `Address: 689/12 ซอยสุขุมวิท 71` → `Address: ***/** ซอยสุขุมวิท 71` | คนที่ 5 | stub |

> รายละเอียดของแต่ละ pattern (พร้อมคำอธิบายทีละส่วน) อยู่ที่ [`docs/regex.md`](docs/regex.md)
> — เจ้าของกฎเป็นคนมาเติมตอน PR ของตัวเอง

---

## API

| Method | Path | คำอธิบาย |
|---|---|---|
| POST | `/api/mask/` | `{"text": "...", "rules": ["email"]}` → `{"masked", "detections", "summary", "total"}` |
| GET | `/api/rules/` | รายชื่อกฎทั้งหมด (frontend เอาไปวาด checkbox) |
| GET | `/api/health/` | health check |

```bash
curl -X POST http://localhost:8000/api/mask/ \
  -H "Content-Type: application/json" \
  -d '{"text": "ติดต่อ somchai@example.com"}'
```

---

## การแบ่งงานและ branch

| # | บทบาท | ไฟล์ที่รับผิดชอบ | branch |
|---|---|---|---|
| 1 | Lead / Integrator | `engine/masker.py`, `engine/base.py`, `registry.py` | `main` + review PR |
| 2 | Regex A | `rules/credit_card.py`, `rules/phone.py` | `feat/rule-card-phone` |
| 3 | Regex B | `rules/email.py` | `feat/rule-email` |
| 4 | Regex C | `rules/dob.py` | `feat/rule-dob` |
| 5 | Regex D | `rules/address.py` | `feat/rule-address` |
| 6 | Frontend | `templates/`, `static/` | `feat/frontend` |
| 7 | Backend + DevOps | `api.py`, `Dockerfile`, deploy, README | `feat/api-deploy` |

รายละเอียดวิธีทำงานร่วมกัน (กฎการ merge, checklist ของ PR) อยู่ที่ [`docs/workflow.md`](docs/workflow.md)

---

## Deploy

ดู [`docs/deploy.md`](docs/deploy.md) — สรุปสั้น ๆ: build ด้วย `--target prod` แล้วรัน gunicorn
ไฟล์ static เสิร์ฟด้วย whitenoise จึงไม่ต้องตั้ง nginx แยก
