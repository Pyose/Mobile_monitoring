# from flask import Flask, request, send_file
# from PIL import Image, ImageDraw
# import io
# from ultralytics import YOLO

# app = Flask(__name__)
# model = YOLO("path/to/your/yolov8n.pt")  # モデルパスを指定

# TARGET_CLASSES = [
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

#     # 特定のクラスの検出結果を抽出して保存
#     target_boxes = []
#     for result in results:
#         for box in result.boxes:
#             class_id = int(box.cls)
#             label = model.names[class_id]
#             confidence = box.conf.item()

#             # 特定のクラスのみを抽出
#             if label in TARGET_CLASSES:
#                 x_min, y_min, x_max, y_max = box.xyxy[0]
#                 target_boxes.append({
#                     "x_min": x_min, "y_min": y_min,
#                     "x_max": x_max, "y_max": y_max,
#                     "label": label, "confidence": confidence
#                 })

#     # バウンディングボックスの重なりをチェックして色を変更
#     draw = ImageDraw.Draw(image)
#     for i, box1 in enumerate(target_boxes):
#         color = "green"  # デフォルトの色
#         for j, box2 in enumerate(target_boxes):
#             if i != j:  # 自分自身でない場合
#                 if is_overlapping(box1, box2):
#                     color = "blue"  # 重なりが検出された場合の色

#         # バウンディングボックスを描画
#         draw.rectangle(((box1["x_min"], box1["y_min"]), (box1["x_max"], box1["y_max"])), outline=color, width=3)
#         draw.text((box1["x_min"], box1["y_min"]), f"{box1['label']} ({box1['confidence']:.2f})", fill=color)

#     # 画像をバイトデータに変換してクライアントに送信
#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)

#     return send_file(img_byte_arr, mimetype='image/png')

# def is_overlapping(box1, box2):
#     """バウンディングボックス同士が重なっているかを判定する関数"""
#     return not (box1["x_max"] < box2["x_min"] or box1["x_min"] > box2["x_max"] or
#                 box1["y_max"] < box2["y_min"] or box1["y_min"] > box2["y_max"])

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
