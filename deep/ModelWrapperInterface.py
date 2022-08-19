class ModelWrapperInterface:

    def __init__(self, device_system):
        self.load_model()
        self.model.eval()

    def to_device(self, device):
        self.model.to(device)
    

