from turtle import forward
from torch.nn.parallel import DistributedDataParallel as DDP
from deep.BLURIFE.SOON import SoonNet
from deep.BLURIFE.RIFE.IFNet import *

class BLURIFE(nn.Module):
    def __init__(self, predictor_weights = None, cleaner_weights = None):
        super(BLURIFE, self).__init__()
        self.predictor = IFNet()
        self.cleaner = SoonNet()
        if predictor_weights != None:
            self.predictor.load_state_dict(predictor_weights)
        if cleaner_weights != None:
            self.cleaner.load_state_dict(cleaner_weights)
    
    def forward(self, input, scale=[4,2,1],timestep=0.5):
        flow, mask, merged, flow_teacher, merged_teacher, loss_distill = self.predictor(input,scale,timestep)
        set = torch.stack((input[:, :3], merged[2]))
        result = self.cleaner(set)
        return flow, mask, merged, flow_teacher, merged_teacher, loss_distill, result

    def inference(self, img0, img1):
        flow, mask, merged, flow_teacher, merged_teacher, loss_distill, result= self.forward(torch.cat((img0, img1), 1))
        return result[1]