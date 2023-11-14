import torch
import math
import torch
import torchvision

from itertools import repeat
from torch import nn as nn
from torch.nn import functional as F
from torch.nn import init as init
from torch.nn.modules.batchnorm import _BatchNorm


class SAFMN:
    def __init__(self, dim_in, dim_out):
        self.embed_dim = dim_out
        self.shallow_conv = nn.Conv2d(dim_in,
                                      dim_out,
                                      kernel_size=3,
                                      padding=1,
                                      stride=1)
        

# CCM
class CCM(nn.Module):
    """
        注意输入的尺度中间是否发生变化操作
    """
    def __init__(self, embed_dim, growth_rate=2.0):
        super().__init__()

        self.embed_dim = embed_dim
        self.conv = nn.Conv2d(embed_dim, embed_dim, 3, 1, 1)
        self.activate = nn.GELU()
        self.conv2 = nn.Conv2d(embed_dim, embed_dim, 1, 1, 0)

    def forward(self, x):
        x = self.activate(self.conv(x))
        x = self.conv2(x)
        return x


class SAFM(nn.Module):
    def __init__(self, embed_dim, n_levels=4):
        super().__init__()
        self.embed_dim = embed_dim
        self.level = n_levels
        self.conv = nn.Conv2d(embed_dim * n_levels, embed_dim, 1, 1, 0)
        self.activate = nn.GELU()

    def forward(self, x):
        original_x = x
        sizes = x.size()[-2:]
        res = []
        for i in range(0, self.level):
            ooutput_size = (int(sizes[0]/2**i), int(sizes[1]/2**i))
            ret = AdaptiveMaxPoolWithDownscaling(ooutput_size, sizes)(x)
            res.append(ret)

        x = torch.cat(res, dim=1)
        x = self.activate(self.conv(x))
        return x @ original_x


class AttBlock:
    def __init__(self, embed_dim):
        self.norm = nn.LayerNorm()
        self.safm = SAFM(embed_dim)
        self.ccm = CCM(embed_dim)

    def forward(self, x):
        x = self.safm(self.norm(x)) + x
        x = self.ccm(self.norm(x)) + x
        return x


class AdaptiveMaxPoolWithDownscaling(nn.Module):
    def __init__(self, output_size, sizes):
        self.sizes = sizes
        super(AdaptiveMaxPoolWithDownscaling, self).__init__()
        self.adaptive_maxpool = nn.AdaptiveMaxPool2d(output_size)

    def forward(self, x):
        sizes = x.size()[-2:]
        x = self.adaptive_maxpool(x)
        x = F.interpolate(x, size=self.sizes, mode='nearest')
        return x

if __name__ == "__main__":
    input_data = torch.randn(1, 3, 128, 128)
    model = SAFM(3)
    output_data = model(input_data)
    print(output_data.size())
