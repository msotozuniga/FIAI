import torch
import torch.nn as nn
import numpy as np
from deep.BLURIFE.ConvLSTM import ConvLSTMCell

def conv(in_planes, out_planes, kernel_size=3, stride=1, padding=1, dilation=1):
    return nn.Sequential(
        nn.Conv2d(in_planes, out_planes, kernel_size=kernel_size, stride=stride,
                  padding=padding, dilation=dilation, bias=True),
        nn.BatchNorm2d(out_planes),
        nn.ReLU()
    )

def conv_transpose(in_planes, out_planes, kernel_size = 3, stride=1, padding=1, output_padding=1, dilation=1):
    return nn.Sequential(
        nn.ConvTranspose2d(in_planes, out_planes, kernel_size=kernel_size, stride=stride,
                  padding=padding, output_padding=output_padding, dilation=dilation, bias=True),
        nn.BatchNorm2d(out_planes),
        nn.ReLU()
    )


class ResBlock(nn.Module):
    def __init__(self,channels):
        super(ResBlock, self).__init__()
        self.rp0 = nn.ReflectionPad2d(1)
        self.conv0 = conv(channels,channels,3,1,0)
        self.rp1 = nn.ReflectionPad2d(1)
        self.conv1 = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=3, stride=1,
                      padding=0, dilation=1, bias=True),
            nn.BatchNorm2d(channels)
        )
        self.relu = nn.ReLU()


    def forward(self,x):
        identity = x
        x = self.rp0(x)
        x = self.conv0(x)
        x = self.rp1(x)
        x = self.conv1(x)
        x = self.relu(x+identity)
        return x

    
class SoonNet(nn.Module):
    def __init__(self):
        super(SoonNet, self).__init__()
        self.set0 = nn.Sequential(
            nn.ReflectionPad2d(3),
            conv(3,16,kernel_size=3,stride=1,padding=0),
            conv(16,32,kernel_size=3,stride=1,padding=0),
            conv(32,64,kernel_size=3,stride=1,padding=0)
        )
        self.set1 = nn.Sequential(
            conv(128,64,kernel_size=3,stride=1,padding=1),
            conv(64,128,kernel_size=3,stride=2,padding=1),
            conv(128,256,kernel_size=3,stride=2,padding=1)
        )
        self.resblocks = nn.Sequential(
            ResBlock(256),
            ResBlock(256),
            ResBlock(256),
            ResBlock(256),
            ResBlock(256),
            ResBlock(256),
            ResBlock(256),
            ResBlock(256),
            ResBlock(256)
        )
        self.convlstm = ConvLSTMCell(256,256,(3,3),True)
        self.set2= nn.Sequential(
            conv_transpose(256,128,kernel_size=3,stride=2,padding=1,dilation=1),
            conv_transpose(128,64,kernel_size=3,stride=2,padding=1,dilation=1)
        )
        self.out = nn.Sequential(
            nn.ReflectionPad2d(3),
            nn.Conv2d(64, 3, kernel_size=7, stride=1, padding=0),
            nn.Tanh()
        )

    def init_features(self, batch_size, channels,image_size,device="cpu"):
        height, width = image_size
        return (torch.zeros(batch_size, channels, height, width, device=device))


    def forward(self, input, p_f = None, conv_cells = None, batch_first = False):
        #TODO pensar como entrenar en batches
        """
        Parameters
        ----------
        input_tensor: todo
            5-D Tensor of shape (t, b, c, h, w)
        p_f: todo
            features from previously procesed image 
        conv_cell: todo
            cells and hidden states for convLSTM of previous iteration
        Returns
        -------
        deblurred_image, feature_map, conv_cells
        """

        if batch_first:
            # (b, t, c, h, w) -> (t, b, c, h, w)
            input = input.permute(1, 0, 2, 3, 4)
        
        result = []
        
        for image in input:
            # x : (b, c, h, w)
            identity = image
            x = self.set0(image)
            b, c, h, w = x.shape
            if p_f is None:
                p_f = self.init_features(b,64, (h,w),x.device)
            x = torch.cat((x,p_f), 1)
            x = self.set1(x)
            x = self.resblocks(x)
            b, _, h, w = x.shape
            if conv_cells is None:
                conv_cells = self.convlstm.init_hidden(b,image_size=(h, w))
            conv_cells = self.convlstm(x, conv_cells)
            x = self.set2(conv_cells[0])
            p_f = x
            x = self.out(x)
            x = identity + x
            result.append(x)
        return torch.stack(result,dim=0)