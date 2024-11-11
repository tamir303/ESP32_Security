import camera
import cam_config as cc

class Camera:
    def __init__(self):
        # Configure and initialize the camera
        camera.conf(cc.FRAMESIZE, cc.FRAMESIZE_QVGA)  # Good for OpenCV
        self.cam = camera.init()
        print("Camera ready?:", self.cam)
        if self.cam:
            self.set_preferences()

    def set_preferences(self):
        # Set camera preferences
        camera.contrast(2)       # Increase contrast
        camera.speffect(2)       # JPEG grayscale

    def capture_image(self):
        return camera.capture() if self.cam else None

    def is_ready(self):
        return self.cam
