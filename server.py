from flask import Flask, request, send_file
import os
import uuid
import cv2
import requests
from realesrgan import RealESRGANer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB limit

MODEL_MAP = {
    'x2': 'RealESRGAN_x2.pth',
    'x4': 'RealESRGAN_x4.pth',
    'x4plus': 'RealESRGAN_x4plus.pth',
    'anime': 'RealESRGAN_x4plus_anime_6B.pth',
    'x8': 'RealESRGAN_x8.pth'
}

MODEL_URLS = {
    'RealESRGAN_x2.pth': 'https://huggingface.co/camsys/Real-ESRGAN/resolve/main/RealESRGAN_x2.pth',
    'RealESRGAN_x4.pth': 'https://huggingface.co/camsys/Real-ESRGAN/resolve/main/RealESRGAN_x4.pth',
    'RealESRGAN_x4plus.pth': 'https://huggingface.co/xinntao/Real-ESRGAN/resolve/main/weights/RealESRGAN_x4plus.pth',
    'RealESRGAN_x4plus_anime_6B.pth': 'https://huggingface.co/xinntao/Real-ESRGAN/resolve/main/weights/RealESRGAN_x4plus_anime_6B.pth',
    'RealESRGAN_x8.pth': 'https://huggingface.co/camsys/Real-ESRGAN/resolve/main/RealESRGAN_x8.pth'
}

def ensure_model_exists(model_path, model_name):
    if not os.path.exists(model_path):
        print(f"Downloading {model_name}...")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        url = MODEL_URLS[model_name]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(model_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

def get_model_path(name):
    model_file = MODEL_MAP.get(name, MODEL_MAP['x4plus'])
    model_path = os.path.join('weights', model_file)
    ensure_model_exists(model_path, model_file)
    return model_path

@app.route('/upscale', methods=['POST'])
def upscale():
    model_key = request.args.get('model', 'x4plus')
    model_path = get_model_path(model_key)

    file = request.files['image']
    img_path = f"temp_{uuid.uuid4()}.png"
    out_path = f"upscaled_{uuid.uuid4()}.png"
    file.save(img_path)

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    upscaler = RealESRGANer(scale=4, model_path=model_path)
    output, _ = upscaler.enhance(img, outscale=4)
    cv2.imwrite(out_path, output)

    os.remove(img_path)
    return send_file(out_path, mimetype='image/png', as_attachment=True)

@app.route('/health')
def health():
    return "OK", 200

# Warmup on startup
@app.before_first_request
def warmup():
    print("Warming up default model...")
    get_model_path('x4plus')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
