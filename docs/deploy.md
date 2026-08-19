# Deploy   [ผู้รับผิดชอบ: คนที่ 7]

## สิ่งที่ต้องมีก่อน

- `DJANGO_SECRET_KEY` แบบสุ่มจริง (ห้ามใช้ค่าใน `.env.example`)
- `DJANGO_SETTINGS_MODULE=config.settings.prod`
- `DJANGO_ALLOWED_HOSTS` และ `DJANGO_CSRF_TRUSTED_ORIGINS` ใส่โดเมนจริง

## Render (มี free tier + ได้ URL จริง)

1. Push repo ขึ้น GitHub (public ตามโจทย์)
2. New → Web Service → เลือก repo → Runtime: **Docker**
3. Dockerfile path: `./Dockerfile`, Docker target: **`prod`**
4. ใส่ environment variables ตามด้านบน
5. Health check path: `/api/health/`

## Hugging Face Spaces (Docker SDK)

สร้าง Space แบบ Docker แล้ววาง `Dockerfile` นี้ได้เลย — แต่ Spaces ฟัง port **7860**
จึงต้องแก้ CMD เป็น `--bind 0.0.0.0:7860` หรือใช้ `$PORT`

## รัน prod image ในเครื่องเพื่อทดสอบก่อน deploy

```bash
docker build --target prod -t pdpa-masking:prod .
docker run --rm -p 8000:8000 \
  -e DJANGO_SECRET_KEY=test-only \
  -e DJANGO_SETTINGS_MODULE=config.settings.prod \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  pdpa-masking:prod
```

## Checklist ก่อนส่งงาน

- [ ] URL เปิดได้จากเครื่องคนนอกทีม
- [ ] หน้าเว็บมีลิงก์ไป GitHub (โจทย์บังคับ)
- [ ] `DEBUG=False` บน production
- [ ] `samples/sample_log.txt` โหลดผ่านปุ่มบนหน้าเว็บได้
