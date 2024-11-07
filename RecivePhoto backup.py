# from flask import Flask, request, send_file
# from PIL import Image, ImageDraw
# import io
# from ultralytics import YOLO

# app = Flask(__name__)
# model = YOLO("path/to/your/yolov8n.pt")  # モデルパスを指定

# # 検出を許可するクラスを定義（例: "person", "car"）
# ALLOWED_CLASSES = [
#                    "refrigerator", "microwave", "tv", "dining table", 
#                    "book", "cup", "bottle"
#                    ]

# @app.route('/upload', methods=['POST'])
# def upload_image():
#     # 受信した画像データを取得
#     image_data = request.data
#     image = Image.open(io.BytesIO(image_data))

#     # YOLOモデルで推論を実行
#     results = model(image)

#     # 検出結果をクラスに基づいてフィルタリング
#     draw = ImageDraw.Draw(image)
#     for result in results:
#         for box in result.boxes:
#             class_id = int(box.cls)
#             label = model.names[class_id]
#             confidence = box.conf.item()

#             # 指定されたクラスのみを処理
#             if label in ALLOWED_CLASSES:
#                 x_min, y_min, x_max, y_max = box.xyxy[0]

#                 # バウンディングボックスを描画
#                 draw.rectangle(((x_min, y_min), (x_max, y_max)), outline="red", width=3)
#                 draw.text((x_min, y_min), f"{label} ({confidence:.2f})", fill="red")

#     # 画像をバイトデータに変換してクライアントに送信
#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)

#     return send_file(img_byte_arr, mimetype='image/png')

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
