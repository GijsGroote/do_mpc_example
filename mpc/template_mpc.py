import do_mpc
from global_variables import *

def template_mpc(model, n_horizon, targetState):


    # Obtain an instance of the do-mpc MPC class
    mpc = do_mpc.controller.MPC(model)
    mpc.targetState = targetState

    # suppress output
    suppress_ipopt = {'ipopt.print_level': 0, 'ipopt.sb': 'yes', 'print_time': 0}
    mpc.set_param(nlpsol_opts=suppress_ipopt)

    # Set parameters:
    setup_mpc = {
        'n_horizon': n_horizon,
        't_step': DT,
        'n_robust': 1,
        'store_full_solution': PLOT_CONTROLLER,
    }

    rterm_u1 = 1e-2
    rterm_u2 = 1e-2
    mpc.set_param(**setup_mpc)


    lterm = (model.x["pos_x"]-model.tvp["pos_x_target"]) ** 2 + \
    (model.x["pos_y"]-model.tvp["pos_y_target"]) ** 2 + \
    0.1*(model.x["ang_p"]-model.tvp["ang_p_target"]) ** 2
    mterm = 0.5*lterm 
     
    mpc.set_objective(mterm=mterm, lterm=lterm)
    mpc.set_rterm(
        u1=rterm_u1,
        u2=rterm_u2
    )

    tvp_template = mpc.get_tvp_template()
    def tvp_fun(t_now):
        for k in range(n_horizon+1):
                tvp_template['_tvp',k,'pos_x_target'] = targetState[0] 
                tvp_template['_tvp',k,'pos_y_target'] = targetState[1] 
                tvp_template['_tvp',k,'ang_p_target'] = targetState[2]

        return tvp_template

    mpc.set_tvp_fun(tvp_fun)

    # Lower bounds on states:
    # mpc.bounds['lower', '_x', 'ang_p'] = -2 * np.pi
    # Upper bounds on states
    # mpc.bounds['upper', '_x', 'ang_p'] = 2 * np.pi

    # Lower bounds on inputs:
    mpc.bounds['lower', '_u', 'u1'] = -1.5
    mpc.bounds['lower', '_u', 'u2'] = -1.5
    # upper bounds on inputs:
    mpc.bounds['upper', '_u', 'u1'] = 1.5
    mpc.bounds['upper', '_u', 'u2'] = 1.5

    mpc.setup()

    return mpc
