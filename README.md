# Smart Traffic Light Management System 🚦

This project is a computer vision-based system designed to optimize traffic light timings in real-time. By utilizing **YOLOv5** for object detection, the system analyzes live video feeds to count vehicles and pedestrians, dynamically adjusting traffic signals to reduce congestion and improve traffic flow. Developed as a final year Software Engineering project.

## Key Features
* 🚗 **Real-time Detection:** Detects vehicles (cars, trucks, buses, motorcycles) and pedestrians with high accuracy using YOLOv5.
* 📊 **Density Analysis:** Calculates traffic density for each lane dynamically.
* ⏱️ **Adaptive Timing:** Automatically adjusts green light duration based on the current traffic load.
* 🎥 **Video Processing:** Capable of processing both pre-recorded video files (e.g., `highway.mp4`) and live camera feeds.

## Technologies Used
* Python 3.x
* YOLOv5 (PyTorch)
* OpenCV
* NumPy / Pandas
