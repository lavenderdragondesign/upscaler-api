# Upscaler API (with Auto-Download + Model Selection)

This is a Flask-based Real-ESRGAN image upscaling API with automatic model downloading, dynamic model selection, and Docker support — ready to deploy on platforms like Render or your own VPS.

---

## 🚀 Features

✅ Auto-downloads `.pth` models from Hugging Face if missing  
✅ Selectable model via `?model=x4`, `?model=anime`, etc.  
✅ Defaults to `x4plus` model  
✅ Docker-ready, deployable on [Render](https://render.com)  
✅ Warmup supported  
✅ File size limits built-in

---

## 🧪 Available Models

| Model Key | Description                             |
|-----------|-----------------------------------------|
| `x2`      | RealESRGAN x2 (mild upscale)            |
| `x4`      | RealESRGAN x4 (standard)                |
| `x4plus`  | RealESRGAN x4+ (default, photorealistic)|
| `x8`      | RealESRGAN x8 (high scale, slow)        |
| `anime`   | RealESRGAN Anime 6B (cartoon art)       |

---

## 🛠 Usage

**POST** an image:

```
POST /upscale?model=x4plus
Form-Data: image=@yourfile.png
```

Returns: upscaled PNG file.

---

## 🐳 Run with Docker

```bash
docker build -t upscaler-api .
docker run -p 5000:5000 upscaler-api
```

---

## 🌐 Deploy to Render

1. Push to GitHub
2. Create a Web Service
3. Use **Docker** environment
4. Set port to `5000`
5. Enable Auto Deploy

---

## 📤 Push to GitHub

```bash
git init
git remote add origin https://github.com/lavenderdragondesign/upscaler-api.git
git add .
git commit -m "Initial commit with auto-download support"
git push -u origin main
```

---

Built with 🪄 by [LavenderDragonDesign](https://www.etsy.com/shop/LavenderDragonDesigns)
