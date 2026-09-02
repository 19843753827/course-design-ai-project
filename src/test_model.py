import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
from model import DefectCNN

model = DefectCNN(num_classes=6)
model.load_state_dict(torch.load('../models/defect_cnn.pth', map_location='cpu'))
model.eval()
print('模型加载成功，参数总量:', sum(p.numel() for p in model.parameters()), '个')
