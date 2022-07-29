from mpc.Mpc import Mpc
import numpy as np
import gym
import urdfenvs.boxer_robot
import urdfenvs.point_robot_urdf
from global_variables import DT


def main():
    
    env = gym.make('boxer-robot-vel-v0', dt=DT, render=True)

    ob = env.reset()
 
    currentState= ob["joint_state"]["position"]
    
    targetState = [1, 0, 0]

    mpc_controller = Mpc()
    mpc_controller.setup(currentState, targetState)


    ob, reward, done, info = env.step(np.array([0.0, 0.0, 0.0]))


    for i in range(1000):

        currentState = ob["joint_state"]["position"]

        action = mpc_controller.respond(currentState)

        ob, _, _, _ = env.step(action)
         
        # multiple target positions
        if i == 50:
            mpc_controller.setTargetState([-2, 1, 0]) 

        if i == 200:
            mpc_controller.setTargetState([3, -1, 0]) 

        if i == 250:
            mpc_controller.setTargetState([3, -1, 3]) 

if __name__ == "__main__":
    main()





