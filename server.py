from flask import Flask, request, send_file
import os
import uuid
import cv2
import requests
from realesrgan import RealESRGANer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # Limit: 20MB uploads

MODEL_NAME = 'RealESRGAN_x4plus.pth'
MODEL_URL = 'https://huggingface.co/xinntao/Real-ESRGAN/resolve/main/weights/RealESRGAN_x4plus.pth'
MODEL_PATH = os.path.join('weights', MODEL_NAME)

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print("Downloading model...")
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(MODEL_PATH, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

@app.before_first_request
def warmup():
    ensure_model()

@app.route('/upscale', methods=['POST'])
def upscale():
    ensure_model()
    file = request.files['image']
    img_path = f"temp_{uuid.uuid4()}.png"
    out_path = f"upscaled_{uuid.uuid4()}.png"
    file.save(img_path)

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    upscaler = RealESRGANer(scale=4, model_path=MODEL_PATH)
    output, _ = upscaler.enhance(img, outscale=4)
    cv2.imwrite(out_path, output)

    os.remove(img_path)
    return send_file(out_path, mimetype='image/png', as_attachment=True)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
