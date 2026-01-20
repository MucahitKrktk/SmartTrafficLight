import cv2
import torch
import numpy as np
from tracker import *

# YOLOv5 modelini yükle
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Video kaynağı
cap = cv2.VideoCapture('highway.mp4')

# Araç ve yaya izleme için gerekli değişkenler
count = 0
vehicle_tracker = Tracker()
pedestrian_tracker = Tracker()

# İzleme alanları (Araçlar ve yayalar için)
vehicle_area = [(275, 445), (275, 485), (530, 485), (530, 445)]
pedestrian_area = [(580, 445), (580, 485), (870, 485), (870, 445)]
vehicle_ids = set()
pedestrian_ids = set()

# Sabit yaya sayısı belirleme (örnek olarak 30)
default_pedestrian_count = 30

def calculate_light_durations(vehicle_count, pedestrian_count):
    # Araç ve yaya yoğunluğuna göre trafik ışığı sürelerini belirler
    base_time = 30  # Sabit süre
    vehicle_weight = 1.5
    pedestrian_weight = 1.0

    vehicle_time = base_time + int(vehicle_weight * vehicle_count)

    # Araç sayısına göre yaya ışık süresini orantılı olarak azalt
    adjusted_pedestrian_time = max(base_time + int(pedestrian_weight * pedestrian_count) - int(0.5 * vehicle_count), 15)

    return vehicle_time, adjusted_pedestrian_time

while True:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 3 != 0:
        continue

    frame = cv2.resize(frame, (1020, 600))

    # YOLOv5 ile tahmin yap
    results = model(frame)

    vehicle_list = []
    pedestrian_list = []

    # Algılanan nesneler üzerinde iterasyon
    for index, rows in results.pandas().xyxy[0].iterrows():
        x, y, x1, y1 = int(rows[0]), int(rows[1]), int(rows[2]), int(rows[3])
        label = str(rows['name'])

        # Araçlar ve yayalar için ayrıştırma
        if label in ['car', 'truck', 'bus', 'motorcycle']:
            vehicle_list.append([x, y, x1, y1])
        elif label in ['person']:
            pedestrian_list.append([x, y, x1, y1])

    # Araç ve yaya takibi
    vehicle_bboxes = vehicle_tracker.update(vehicle_list)
    pedestrian_bboxes = pedestrian_tracker.update(pedestrian_list)

    # İzleme kutucuklarını çiz ve alanlara göre ID'leri topla
    for bbox in vehicle_bboxes:
        x2, y2, x3, y3, obj_id = bbox
        cv2.rectangle(frame, (x2, y2), (x3, y3), (0, 0, 255), 2)
        cv2.putText(frame, f'V{obj_id}', (x2, y2 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        result = cv2.pointPolygonTest(np.array(vehicle_area, np.int32), (x3, y3), False)
        if result > 0:
            vehicle_ids.add(obj_id)

    for bbox in pedestrian_bboxes:
        x2, y2, x3, y3, obj_id = bbox
        cv2.rectangle(frame, (x2, y2), (x3, y3), (0, 255, 0), 2)
        cv2.putText(frame, f'P{obj_id}', (x2, y2 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        result = cv2.pointPolygonTest(np.array(pedestrian_area, np.int32), (x3, y3), False)
        if result > 0:
            pedestrian_ids.add(obj_id)

    # Yoğunluk bilgilerini hesapla
    vehicle_count = len(vehicle_ids)

    # Algılanan yaya sayısı yoksa sabit değer kullan
    pedestrian_count = len(pedestrian_ids) if len(pedestrian_ids) > 0 else default_pedestrian_count

    vehicle_time, pedestrian_time = calculate_light_durations(vehicle_count, pedestrian_count)

    # Terminal çıktısı
    print(f"Frame {count}:")
    print(f"  Vehicle Count: {vehicle_count}")
    print(f"  Pedestrian Count: {pedestrian_count}")
    print(f"  Vehicle Light Duration: {vehicle_time} seconds")
    print(f"  Pedestrian Light Duration: {pedestrian_time} seconds")
    print("-" * 50)

    # Ekrana çizim yap
    cv2.polylines(frame, [np.array(vehicle_area, np.int32)], True, (255, 255, 0), 2)
    cv2.polylines(frame, [np.array(pedestrian_area, np.int32)], True, (255, 255, 0), 2)

    cv2.putText(frame, f'Vehicles: {vehicle_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Pedestrians: {pedestrian_count}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Vehicle Light: {vehicle_time}s', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Pedestrian Light: {pedestrian_time}s', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("FRAME", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
