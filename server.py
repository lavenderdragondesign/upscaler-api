from flask import Flask, request, send_file
import os
import uuid
import cv2
from realesrgan import RealESRGANer

app = Flask(__name__)
upscaler = RealESRGANer(scale=4, model_path='weights/RealESRGAN_x4plus.pth')

@app.route('/upscale', methods=['POST'])
def upscale():
    file = request.files['image']
    img_path = f"temp_{uuid.uuid4()}.png"
    out_path = f"upscaled_{uuid.uuid4()}.png"
    file.save(img_path)

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    output, _ = upscaler.enhance(img, outscale=4)
    cv2.imwrite(out_path, output)

    os.remove(img_path)
    return send_file(out_path, mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
