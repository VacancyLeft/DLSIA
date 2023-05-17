import torch
import utility as ut
import AENet
import AE2
import numpy as np

def NeurualNetwork(V_x, len_Om, l_rate, epoch, hidden_num, N, k, alpha, Om, nodes, a, o, gamma, weight_decay=1.0):
    x = ut.getXvectorsToMatrix(V_x, N, k, len_Om)
    # x = {{1.0},{0.10836802322189586}, {0.10836802322189586},{1.0},
    #      {0.10836802322189586},{0.10836802322189586},{0.10836802322189586},{0.10836802322189586},
    #      {0.01174362845702136},{0.01174362845702136},{0.01174362845702136},{0.01174362845702136},{1.0},{1.0},{1.0},{0.0013},{0.0013}}
# [1.0, 0.10836802322189586, 0.10836802322189586, 0.10836802322189586, 0.10836802322189586, 0.01174362845702136, 1.0, 0.01174362845702136, 0.01174362845702136, 0.01174362845702136, 0.01174362845702136, 0.01174362845702136, 0.01174362845702136, 0.001272633801339809, 0.001272633801339809]
    x_new = ut.getReshapeMatrix(x, N, k, len_Om)
    x = torch.tensor(x, dtype = float)
    x_new = torch.tensor(x_new, dtype=float)
    # targets = torch.tensor(x, dtype=float)
    # targets = torch.tensor(x_new, dtype = float)
    # initial
    AE = AENet.AutoEncoder(N, k, len_Om,hidden_num)
    criterion = AENet.LossFunction(alpha,Om, nodes, x, a, o)
    if weight_decay > 0:
        reg_loss = AENet.Regularization(AE, weight_decay, p=2)
    with open('loss_z.txt', 'a') as f:
        f.write(str(a))
        f.write('\n')
    # AE = AE2.AutoEncoder(N, k, len_Om, hidden_num)
    # criterion = AE2.LossFunction(alpha, Om, nodes, x)
    # if weight_decay > 0:
    #     reg_loss = AE2.Regularization(AE, weight_decay, p=2)
    optimizer = torch.optim.Adam(AE.parameters(), l_rate)
    z = torch.empty(N, k)
    for ep in range(epoch):
        inputs = x_new
        z, x_hat= AE(inputs)
        x_hat_t = x_hat.t()
        z_t = z.t()
        loss = criterion (x_new, z, x_hat)
        if weight_decay > 0:
            loss_reg = reg_loss(AE)
        loss = loss + gamma*loss_reg
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        z = z_t
        print(z)
    with open('data_z.txt', 'w') as f:
        trans = z.detach().numpy()
        np.savetxt('data_z.txt', trans, fmt='%f', delimiter=',')
        pass
    return z_t