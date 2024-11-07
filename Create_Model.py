import torch
from dataset import CustomDataset
from model import create_model
from utils import get_optimizer, train_model

import os

label_data = []

# 画像ファイルと対応するラベルファイルのディレクトリ
image_dir = 'C:/Furniture.v2i.yolov8/train/images'
label_dir = 'C:/Furniture.v2i.yolov8/train/labels'

# 画像ファイルのリストを取得し、対応するラベルファイルを読み込む
image_files = sorted(os.listdir(image_dir))

for image_file in image_files:
    # ラベルファイルのパスを生成
    label_file_path = os.path.join(label_dir, image_file.replace('.jpg', '.txt'))
    
    boxes = []
    labels = []
    
    # ラベルファイルが存在する場合に読み込む
    if os.path.exists(label_file_path):
        with open(label_file_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                class_label = int(values[0])
                x_center = float(values[1])
                y_center = float(values[2])
                width = float(values[3])
                height = float(values[4])

                # 相対座標を絶対座標に変換（例: 画像サイズが 640x480 の場合）
                img_width, img_height = 640, 480  # 画像の幅と高さ
                xmin = (x_center - width / 2) * img_width
                ymin = (y_center - height / 2) * img_height
                xmax = (x_center + width / 2) * img_width
                ymax = (y_center + height / 2) * img_height
                
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(class_label)

    # 各画像のボックスとラベルを追加
    label_data.append((boxes, labels))

# 結果の確認
#print(label_data)

# デバイスの設定
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# データセットとデータローダーの設定
dataset = CustomDataset(image_dir, label_data)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=True, collate_fn=lambda x: tuple(zip(*x)))

# モデルの構築とオプティマイザの設定
model = create_model(num_classes=10).to(device)
optimizer = get_optimizer(model)

# 学習ループの開始
train_model(model, data_loader, optimizer, device)
