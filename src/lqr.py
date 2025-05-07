import numpy as np
def f(x, u):
    return x + u
def f_x(x, u):
    return np.eye(len(x))
def f_u(x, u):
    return np.eye(len(u))

def ilqr(f, f_x, f_u, Q, R, Qf, N, x0, u0, target):
    nx = x0.shape[0]
    nu = u0.shape[1]

    x_opt = np.zeros((N + 1, nx))
    u_opt = np.zeros((N, nu))

    x_opt[0] = x0
    u_opt[:] = u0

    for k in range(100):  # Max iterations
        # Forward pass
        for t in range(N):
            x_opt[t + 1] = f(x_opt[t], u_opt[t])

        # Backward pass
        V_x = Qf @ (x_opt[-1] - target)
        V_xx = Qf

        K = np.zeros((N, nu, nx))
        d = np.zeros((N, nu))

        for t in reversed(range(N)):
            fxt = f_x(x_opt[t], u_opt[t])
            fut = f_u(x_opt[t], u_opt[t])

            Q_x = Q @ (x_opt[t] - target) + fxt.T @ V_x
            Q_u = R @ u_opt[t] + fut.T @ V_x

            Q_xx = Q + fxt.T @ V_xx @ fxt
            Q_uu = R + fut.T @ V_xx @ fut
            Q_ux = fut.T @ V_xx @ fxt

            K[t] = -np.linalg.solve(Q_uu, Q_ux)
            d[t] = -np.linalg.solve(Q_uu, Q_u)

            V_x = Q_x + K[t].T @ Q_uu @ d[t]
            V_xx = Q_xx + K[t].T @ Q_uu @ K[t]

        # Update control
        for t in range(N):
            u_opt[t] += K[t] @ (x_opt[t] - x0) + d[t]

    return x_opt, u_opt

def ilqr_path_planner(start, goal, N=50):
    x0 = np.array(start)
    target = np.array(goal)
    u0 = np.random.randn(N, 2) * 0.1
    Q = np.eye(2) * 1.0
    R = np.eye(2) * 0.1
    Qf = np.eye(2) * 10.0
    x_opt, _ = ilqr(f, f_x, f_u, Q, R, Qf, N, x0, u0, target)
    return x_opt