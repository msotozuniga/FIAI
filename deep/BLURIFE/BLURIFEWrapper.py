from tqdm import tqdm

from deep.ModelWrapperAbstract import ModelWrapperAbstract
from deep.BLURIFE.blurife import BLURIFE
import numpy as np
from math import exp
import torch
from torch.nn import functional as F


def gaussian(window_size, sigma):
    gauss = torch.Tensor([exp(-(x - window_size // 2) ** 2 / float(2 * sigma ** 2)) for x in range(window_size)])
    return gauss / gauss.sum()

def create_window_3d(window_size, channel=1,device=torch.device('cpu')):
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t())
    _3D_window = _2D_window.unsqueeze(2) @ (_1D_window.t())
    window = _3D_window.expand(1, channel, window_size, window_size, window_size).contiguous().to(device)
    return window

def ssim_matlab(img1, img2, window_size=11, window=None, size_average=True, full=False, val_range=None):
    # Value range can be different from 255. Other common ranges are 1 (sigmoid) and 2 (tanh).
    if val_range is None:
        if torch.max(img1) > 128:
            max_val = 255
        else:
            max_val = 1

        if torch.min(img1) < -0.5:
            min_val = -1
        else:
            min_val = 0
        L = max_val - min_val
    else:
        L = val_range

    padd = 0
    (_, _, height, width) = img1.size()
    if window is None:
        real_size = min(window_size, height, width)
        window = create_window_3d(real_size, channel=1,device=img1.device).to(img1.device)
        # Channel is set to 1 since we consider color images as volumetric images

    img1 = img1.unsqueeze(1)
    img2 = img2.unsqueeze(1)

    mu1 = F.conv3d(F.pad(img1, (5, 5, 5, 5, 5, 5), mode='replicate'), window, padding=padd, groups=1)
    mu2 = F.conv3d(F.pad(img2, (5, 5, 5, 5, 5, 5), mode='replicate'), window, padding=padd, groups=1)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1 * mu2

    sigma1_sq = F.conv3d(F.pad(img1 * img1, (5, 5, 5, 5, 5, 5), 'replicate'), window, padding=padd,
                         groups=1) - mu1_sq
    sigma2_sq = F.conv3d(F.pad(img2 * img2, (5, 5, 5, 5, 5, 5), 'replicate'), window, padding=padd,
                         groups=1) - mu2_sq
    sigma12 = F.conv3d(F.pad(img1 * img2, (5, 5, 5, 5, 5, 5), 'replicate'), window, padding=padd,
                       groups=1) - mu1_mu2

    C1 = (0.01 * L) ** 2
    C2 = (0.03 * L) ** 2

    v1 = 2.0 * sigma12 + C2
    v2 = sigma1_sq + sigma2_sq + C2
    cs = torch.mean(v1 / v2)  # contrast sensitivity

    ssim_map = ((2 * mu1_mu2 + C1) * v1) / ((mu1_sq + mu2_sq + C1) * v2)

    if size_average:
        ret = ssim_map.mean()
    else:
        ret = ssim_map.mean(1).mean(1).mean(1)

    if full:
        return ret, cs
    return ret


class BLURIFEWrapper(ModelWrapperAbstract):

    def __init__(self, device_system='cpu'):
        super(BLURIFEWrapper,self).__init__(model = BLURIFE(), id= 2, device_system=device_system)


    def load_model(self):
        path = "deep/BLURIFE"
        a = torch.load('{}/Blurife_gopro.pth'.format(path),map_location=self.device_system)
        self.model.load_state_dict(a['model'])


    #TODO arreglar para que se añada las imagenes originales
    def interpolate(self, frames, h, w, intermediates_frames):
        tmp = 32
        ph = ((h - 1) // tmp + 1) * tmp
        pw = ((w - 1) // tmp + 1) * tmp
        padding = (int((ph - h)/2), int((ph - h)/2),int((pw - w)/2), int((pw - w)/2),)
        pader = torch.nn.ReplicationPad2d(padding) 
        exit = []  # [frames[0].numpy()]#
        for i in tqdm(range(len(frames) - 1)):
            exit.append(frames[i])
            I0 = (torch.tensor(frames[i].transpose(2, 0, 1) / 255.)).to(self.device_system).float().unsqueeze(0)
            I1 = (torch.tensor(frames[i+1].transpose(2, 0, 1) / 255.)).to(self.device_system).float().unsqueeze(0)
            I0 = pader(I0)
            I1 = pader(I1)
            output = self.make_inference(I0, I1, intermediates_frames,padding)
            exit.extend(output)
        set = np.stack(exit)
        return set

    def make_inference(self, I0, I1, n,padding):
        middle = self.model.inference(I0, I1)
        if n == 1:
            if padding[0]!=0:
                pred = middle[0][padding[0]:-1*padding[1]]
            if padding[2]!=0:
                pred = middle[0][:,padding[2]:-1*padding[3]]
            return [(((pred * 255.).byte().cpu().numpy().transpose(1, 2, 0)))]
        first_half = self.make_inference(I0, middle, n//2,padding)
        second_half = self.make_inference(middle, I1, n//2,padding)
        if padding[0]!=0:
            pred = middle[0][padding[0]:-1*padding[1]]
        if padding[2]!=0:
            pred = middle[0][:,padding[2]:-1*padding[3]]
        middle= [(((pred * 255.).byte().cpu().numpy().transpose(1, 2, 0)))]
        if n%2:
            return [*first_half, middle, *second_half]
        else:
            return [*first_half, *second_half]