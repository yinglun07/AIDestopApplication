import cv2

class VisionMCPServer:

    def detect_objects(self, video_path):
        cap = cv2.VideoCapture(video_path)

        detected = set()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # FAKE placeholder logic 
            # Example: pretend we detect "person"
            detected.add("person")

        cap.release()

        return list(detected)

    def describe_scene(self, video_path):
        return "A person is visible in the video."
