import camera
import cam_config as cc
from time import sleep
from logger import Logger

log = Logger(name="Camera_Module", level="DEBUG")

class Camera:
    def __init__(self):
        # Configure and initialize the camera
        camera.conf(cc.FRAMESIZE, cc.FRAMESIZE_QVGA)  # Good for OpenCV
        cc.configure(camera, cc.ai_thinker)
        self.cam = camera.init()
        log.info("Initializing camera...")
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
    
    def __enter__(self):
        if not self.is_ready():
            for attempt in range(5):
                self.cam = camera.init()
                # Camera is ready, set configurations and return ref
                if self.is_ready():
                    log.info(f"Successfully connected to camera.")
                    self.set_preferences()
                    return self
                # Camera isn't ready, retry init
                else:
                    log.debug(f"Attempt {attempt + 1} failed. Retrying...")
                    sleep(1)
            raise RuntimeError("Failed to initialize the camera.")
        else:
            log.info(f"Successfully connected to Camera")
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass