import numpy as np

def rollout_error(true_traj, pred_traj, horizon=None):
    if horizon is None:
        horizon = len(true_traj)

    true_traj = true_traj[:horizon]
    pred_traj = pred_traj[:horizon]

    return np.mean(np.linalg.norm(true_traj - pred_traj, axis=1))
