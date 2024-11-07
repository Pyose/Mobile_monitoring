from ultralytics import YOLO

from ultralytics import YOLO

# モデルをロード
model = YOLO("path/to/your/yolov8n.pt")  # モデルパスを指定

# model.namesが辞書形式かどうか確認
print("Model Names Type:", type(model.names))

# クラス情報を詳細に出力
print("Model Class Names:", model.names)

