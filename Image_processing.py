import cv2
import os

class ImageProcessor:
    def __init__(self):
    
        self.original_image = None
        self.image= None
        self.filename = None

    def load_image(self, path):
        self.original_image = cv2.imread(path)
        self.image = self.original_image.copy()
        self.filename = os.path.basename(path)

    def reset_to_original(self):
        self.image = self.original_image.copy()

    def to_grayscale(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    def blur(self, intensity):
        if intensity > 0:
            k = intensity * 2 + 1
            self.image = cv2.GaussianBlur(self.image, (k, k), 0)

    def edge_detection(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        self.image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def adjust_brightness(self, value):
        self.image = cv2.convertScaleAbs(self.image, beta=value)

