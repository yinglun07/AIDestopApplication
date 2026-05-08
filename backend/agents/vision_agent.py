import cv2
import numpy as np
import openvino as ov
core = ov.Core()


class VisionAgent:
    def __init__(self):
        # Load OpenVINO model
        self.core = ov.Core()

        model_path = "yolov8n_openvino_model/yolov8n.xml"
        self.model = self.core.read_model(model=model_path)
        self.compiled_model = self.core.compile_model(self.model, "CPU")

        self.input_layer = self.compiled_model.input(0)
        self.output_layer = self.compiled_model.output(0)

        # COCO labels (YOLO trained classes)
        self.labels = [
            "person", "bicycle", "car", "motorbike", "aeroplane",
            "bus", "train", "truck", "boat", "traffic light",
            "fire hydrant", "stop sign", "parking meter", "bench",
            "bird", "cat", "dog", "horse", "sheep", "cow",
            "elephant", "bear", "zebra", "giraffe", "backpack",
            "umbrella", "handbag", "tie", "suitcase", "frisbee",
            "skis", "snowboard", "sports ball", "kite", "baseball bat",
            "baseball glove", "skateboard", "surfboard", "tennis racket",
            "bottle", "wine glass", "cup", "fork", "knife", "spoon",
            "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
            "carrot", "hot dog", "pizza", "donut", "cake", "chair",
            "sofa", "potted plant", "bed", "dining table", "toilet",
            "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
            "microwave", "oven", "toaster", "sink", "refrigerator",
            "book", "clock", "vase", "scissors", "teddy bear",
            "hair drier", "toothbrush"
        ]

    def analyze(self, file_path: str):

        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()

        if not ret:
            return {"error": "Could not read video"}

        # resize for model
        input_img = cv2.resize(frame, (640, 640))
        input_img = input_img.transpose(2, 0, 1)
        input_img = np.expand_dims(input_img, axis=0)

        # inference
        result = self.compiled_model([input_img])[self.output_layer]

        detected_objects = []

        # parse detections
        for detection in result[0]:
            confidence = float(detection[4])

            if confidence > 0.4:
                class_id = int(detection[5])
                label = self.labels[class_id]
                detected_objects.append(label)

        detected_objects = list(set(detected_objects))

        # simple reasoning layer (for assignment)
        has_graph = any(x in detected_objects for x in ["tv", "laptop", "book"])

        return {
            "objects": detected_objects,
        }