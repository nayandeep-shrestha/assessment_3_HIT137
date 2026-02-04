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