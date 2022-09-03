import torch
from deep.RIFE.warplayer import warp
from torch.nn.parallel import DistributedDataParallel as DDP
from deep.RIFE.IFNet import *
from deep.RIFE.refine import *

    
class Model:
    def __init__(self, local_rank=-1, arbitrary=False, fine_tune = False):
        self.flownet = IFNet()

    def eval(self):
        self.flownet.eval()

    def to(self,device):
        self.flownet.to(device)

    def load_model(self, path, rank=0, m = True, device = "cpu"):
        def convert(param):
            return {
            k.replace("module.", ""): v
                for k, v in param.items()
                if "module." in k
            }
            
        if rank <= 0 and m == True:
            self.flownet.load_state_dict(convert(torch.load('{}/flownet.pkl'.format(path),map_location=device)))
        else:
            self.flownet.load_state_dict(torch.load('{}/flownet.pkl'.format(path),map_location=device))

    def inference(self, img0, img1, scale_list=[4, 2, 1], TTA=False, timestep=0.5):
        imgs = torch.cat((img0, img1), 1)
        flow, mask, merged, flow_teacher, merged_teacher, loss_distill = self.flownet(imgs, scale_list, timestep=timestep)
        if TTA == False:
            return merged[2]
        else:
            flow2, mask2, merged2, flow_teacher2, merged_teacher2, loss_distill2 = self.flownet(imgs.flip(2).flip(3), scale_list, timestep=timestep)
            return (merged[2] + merged2[2].flip(2).flip(3)) / 2
    
