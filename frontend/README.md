# Webui สำหรับ 01204322-Term-Project-Train-Stop

## Setup

1. clone repo 
2. install dependencies (ต้องการ pnpm หากไม่มี `npm install -g pnpm`)
```bash
pnpm install
```
3. ตั้งค่า `.env` (copy `.env.example` แล้วแก้ชื่อไฟล์เป็น `.env`)

```
VITE_MQTT_BROKER = 
VITE_PORT = 9001
VITE_USERNAME = 
VITE_PASS = 
VITE_CROSSINGID = "crossing1"
```

4. `pnpm run build` สำหรับ build project
5. `npx serve dist` เพื่อ run webui 