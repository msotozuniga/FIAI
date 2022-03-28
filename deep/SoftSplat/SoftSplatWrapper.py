
from deep.ModelWrapperInterface import ModelWrapperInterface

class SoftSplatWrapper(ModelWrapperInterface):

    def __init__(self, device_system='cpu'):
        pass


    def load_model(self):
        pass


    def to_device(self, device):
        pass

    def interpolate(self, frames, h, w, intermediates_frames):
        pass