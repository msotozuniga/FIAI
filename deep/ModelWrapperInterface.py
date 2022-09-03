class ModelWrapperAbstract:

    def __init__(self, model, id,device_system):
        self.id = id
        self.model = model
        self.load_model()
        self.to_device(device_system)
        self.model.eval()
        self.device_system = device_system

    def to_device(self, device):
        self.model.to(device)
        self.device_system = device

    def get_id(self):
        return self.id

    def load_model(self):
        pass
    

