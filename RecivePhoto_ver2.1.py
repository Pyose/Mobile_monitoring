from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import io
from ultralytics import YOLO
import os

app = Flask(__name__)
model = YOLO("path/to/your/yolov8n.pt")  # モデルパスを指定

# 対象のクラスを定義
TARGET_CLASSES = [
                   "refrigerator", "microwave", "tv", "dining table", 
                   "book", "cup", "bottle"
                  ]
BASE_CLASSES = ["refrigerator", "dining table"]
TOP_CLASSES = ["book", "cup", "bottle"]

# 保存先のディレクトリ
output_dir = "C:\\Monitoring_ap"

# ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_next_filename(directory, base_name="inference_result", ext=".png"):
    """指定ディレクトリ内で連番ファイル名を取得"""
    existing_files = [f for f in os.listdir(directory) if f.startswith(base_name) and f.endswith(ext)]
    numbers = [int(f[len(base_name):-len(ext)].strip("_")) for f in existing_files if f[len(base_name):-len(ext)].strip("_").isdigit()]
    next_number = max(numbers, default=0) + 1
    return os.path.join(directory, f"{base_name}_{next_number}{ext}")

@app.route('/upload', methods=['POST'])
def upload_image():
    # 受信した画像データを取得
    image_data = request.data
    image = Image.open(io.BytesIO(image_data))

    # YOLOモデルで推論を実行
    results = model(image)

    target_boxes = []
    base_boxes = []
    top_boxes = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)
            label = model.names[class_id]
            confidence = box.conf.item()

            x_min, y_min, x_max, y_max = box.xyxy[0]
            box_data= {
                "x_min": x_min, "y_min": y_min,
                "x_max": x_max, "y_max": y_max,
                "label": label, "confidence": confidence
            }

            if label in BASE_CLASSES:
                base_boxes.append(box_data)
            elif label in TOP_CLASSES:
                top_boxes.append(box_data)

            if label in TARGET_CLASSES:
                target_boxes.append(box_data)

    # 検出結果をクラスごとに分類して保存
    
    # for result in results:
    #     for box in result.boxes:
    #         class_id = int(box.cls)
    #         label = model.names[class_id]
    #         confidence = box.conf.item()

    #         x_min, y_min, x_max, y_max = box.xyxy[0]
    #         box_data = {
    #             "x_min": x_min, "y_min": y_min,
    #             "x_max": x_max, "y_max": y_max,
    #             "label": label, "confidence": confidence
    #         }

    #         if label in BASE_CLASSES:
    #             base_boxes.append(box_data)
    #         elif label in TOP_CLASSES:
    #             top_boxes.append(box_data)

    draw = ImageDraw.Draw(image)

    # 特定のオブジェクトの上に他のオブジェクトがあるかを判定
    if (base_boxes != 0 or top_boxes != 0):
        for base_box in base_boxes:
            for top_box in top_boxes:
                # 上部オブジェクトの下端が下部オブジェクトの上端より上にあるか確認
                if (base_box["y_min"] - top_box["y_max"] <= 100) and top_box["y_max"] <= base_box["y_min"] or ((top_box["y_max"] >= base_box["y_min"] and top_box["y_min"] <= base_box["y_min"]) or top_box["y_min"] >= base_box["y_min"]):
                    # 上部オブジェクトと下部オブジェクトの色を変更
                    draw.rectangle(((top_box["x_min"], top_box["y_min"]), (top_box["x_max"], top_box["y_max"])), outline="yellow", width=3)
                    draw.text((top_box["x_min"], top_box["y_min"]), f"{top_box['label']} ({top_box['confidence']:.2f})", fill="yellow")

                    draw.rectangle(((base_box["x_min"], base_box["y_min"]), (base_box["x_max"], base_box["y_max"])), outline="red", width=3)
                    draw.text((base_box["x_min"], base_box["y_min"]), f"{base_box['label']} ({base_box['confidence']:.2f})", fill="red")
                
                else:
                    draw.rectangle(((top_box["x_min"], top_box["y_min"]), (top_box["x_max"], top_box["y_max"])), outline="green", width=3)
                    draw.text((top_box["x_min"], top_box["y_min"]), f"{top_box['label']} ({top_box['confidence']:.2f})", fill="green")

                    draw.rectangle(((base_box["x_min"], base_box["y_min"]), (base_box["x_max"], base_box["y_max"])), outline="green", width=3)
                    draw.text((base_box["x_min"], base_box["y_min"]), f"{base_box['label']} ({base_box['confidence']:.2f})", fill="green")
    if not base_boxes or not top_boxes:  # どちらか片方のクラスのみ検出された場合
        for target_box in target_boxes:
            draw.rectangle(((target_box["x_min"], target_box["y_min"]), (target_box["x_max"], target_box["y_max"])), outline="green", width=3)
            draw.text((target_box["x_min"], target_box["y_min"]), f"{target_box['label']} ({target_box['confidence']:.2f})", fill="green")


    # ファイル名を生成して画像を保存
    output_path = get_next_filename(output_dir)
    image.save(output_path, format='PNG')

    # 画像をバイトデータに変換してクライアントに送信
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
