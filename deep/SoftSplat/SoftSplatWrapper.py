import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from deep.ModelWrapperInterface import ModelWrapperInterface
from deep.SoftSplat.SoftSplatModel import SoftSplatBaseline
from torchvision.transforms.functional import to_tensor, to_pil_image

class SoftSplatWrapper(ModelWrapperInterface):

    def __init__(self, device_system='cpu'):
        self.model = SoftSplatBaseline(device = device_system)
        super().__init__(device_system=device_system)


    def load_model(self):
        path = r"C:\Users\matia\Documents\Universidad\T-Titulo\Project\deep\RIFE"
        self.model.load_state_dict(torch.load('{}/SOON.pht'.format(path),map_location=self.model.device_system))


    def to_device(self, device):
        self.model.to(device)

    def interpolate(self, frames, h, w, intermediates_frames):
        frames = frames[:, :, :, ::-1] 
        exit = []  # [frames[0].numpy()]#
        I1 = to_tensor(frames[0])
        for i in tqdm(range(1,len(frames) - 1)):
            I0 = I1
            exit.append(np.array(to_pil_image(I1,'RGB')))
            I1 = to_tensor(frames[i])
            batch = torch.stack([I0, I1], dim=1)
            batch = batch[None,:,:,:,:]
            batch = batch.to(self.model.device_system,non_blocking=True).float()

            
            output = self.make_inference(batch, intermediates_frames)
            exit.append(*output)
            # output.append(frames[i+1].numpy())
        exit.append(frames[-1])
        set = np.stack(exit)
        set = set[:, :h, :w, ::-1]
        return set
    
    def make_inference(self, batch, n):
        t = np.arange(1/(n+1), 1, 1/(n+1))
        out = []
        for target_t in t:
            target = torch.tensor([target_t]).to(self.model.device_system)
            middle = self.model(batch,target)
            pred = to_pil_image(middle[0],'RGB')
            temp = np.array(pred)
            out.append(temp)
        return out

    '''
Codigo para crear una imagen interpolada
        img0 = (path + d + '/frame1.png')
        img1 = (path + d + '/frame3.png')
        gt = (path + d + '/frame2.png')

        im0 = Image.open(img0).convert('RGB')
        im1 = Image.open(img1).convert('RGB')
        gt = Image.open(gt).convert('RGB')

        im0 = to_tensor(im0)
        im1 = to_tensor(im1)
        gt = to_tensor(gt)
        batch = torch.stack([im0, im1], dim=1)
        
        batch = batch[None,:,:,:,:]
        batch = batch.cuda().float()
        #batch = batch[None,:,:,:,:]
        
        #batch = torch.cat((img0,img1),2)
        pred = model(batch, target_t)
        print(pred[0].shape)
        pred = to_pil_image(pred[0],'RGB')
        temp = np.array(pred)[:,:,::-1]

'''