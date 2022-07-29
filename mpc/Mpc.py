import do_mpc
import numpy as np
from mpc.template_model import template_model
from mpc.template_mpc import template_mpc
from mpc.template_simulator import template_simulator
# from mpc.template_plotter import Plotter
from global_variables import *

class Mpc():

    def __init__(self):
        self.mpc = None
        self.model = None
        self.simulator = None
        # self.plotter = None
        self.n_horizon = 15


    def setup(self, currentState, targetState):

        # fully define model
        self.model = template_model()

        # set all mpc parameters
        self.mpc = template_mpc(self.model, self.n_horizon, targetState)
        
        x0 = currentState
        self.mpc.x0 = x0

        self.mpc.set_initial_guess()

        
        if PLOT_CONTROLLER:
            self.dt_counter = 0

            simulator = do_mpc.simulator.Simulator(self.model)
            tvp_template = simulator.get_tvp_template()

            def tvp_fun(t_now):
                tvp_template['pos_x_target'] = targetState[0] 
                tvp_template['pos_y_target'] = targetState[1] 
                tvp_template['ang_p_target'] = targetState[2]

                return tvp_template

            simulator.set_tvp_fun(tvp_fun)


            # Set parameter(s):
            simulator.set_param(t_step=DT)
            simulator.setup()

            # just to be sure
            simulator.reset_history()

            simulator.x0 = x0

            self.simulator = simulator
            # self.plotter = Plotter()
            # self.plotter.setup(self.mpc, self.simulator)
        
        self.mpc.reset_history()
            
        
    def respond(self, currentState):
        x0 = currentState
        self.mpc.x0 = x0 
        u0 = self.mpc.make_step(x0) # solves minimisation problem 

        if PLOT_CONTROLLER: 
            self.simulator.x0 = x0
            x0_predict = self.simulator.make_step(u0) 
            self.dt_counter = self.dt_counter +1

        return u0

    def visualise(self):
        # self.plotter.visualise()
        print("NO PLOTTING !")
       
    def setTargetState(self, state):
        tvp_template = self.mpc.get_tvp_template()

        def tvp_fun(t_now):
            for k in range(self.n_horizon+1):
                tvp_template['_tvp',k,'pos_x_target'] = state[0] 
                tvp_template['_tvp',k,'pos_y_target'] = state[1] 
                tvp_template['_tvp',k,'ang_p_target'] = state[2]

            return tvp_template

        self.mpc.set_tvp_fun(tvp_fun)






