import torch

import utility
import data
import model
import loss
from option import args
from trainer import Trainer

from torch import nn

device_ids = [0, 1]



torch.manual_seed(args.seed)
checkpoint = utility.checkpoint(args)
torch.cuda.set_device(0)

if checkpoint.ok:
    loader = data.Data(args)
    model = model.Model(args, checkpoint)
    # model.model.load_state_dict(torch.load('res_greccr2b_2m50_l2/model/model_best.pt'))
    model = nn.DataParallel(module=model, device_ids=device_ids)
    loss = loss.Loss(args, checkpoint) if not args.test_only else None
    t = Trainer(args, loader, model, loss, checkpoint)
    while not t.terminate():
        t.train()
        t.test()

    checkpoint.done()

