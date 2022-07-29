# import do_mpc
# from plotly.subplots import make_subplots
# import plotly.express as px
# import numpy as np
# import plotly.graph_objects as go
# import os
# import pyarrow.feather as feather
# from numpy import dstack
# from robot_brain.global_variables import * 
#
#
# class Plotter():
#
#     def __init__(self):
#         self.simulator = None
#         self.mpc = None
#
#     def setup(self, mpc, simulator):
#         self.mpc = mpc
#         self.simulator = simulator
#
#          
#     def visualise(self):
#         x_ref= self.mpc.targetState.pos[0]
#         y_ref= self.mpc.targetState.pos[1]
#         theta_ref =  self.mpc.targetState.ang_p[2]
#         # x = [i[0] for i in self.simulator.data["_x"]]
#         # y = [i[1] for i in self.simulator.data["_x"]]
#         # theta = [i[2] for i in self.simulator.data["_x"]]
#         # u1 = [i[0] for i in self.simulator.data['_u']]
#         # u2 = [i[1] for i in self.simulator.data['_u']]
#         x = [i[0] for i in self.mpc.data["_x"]]
#         y = [i[1] for i in self.mpc.data["_x"]]
#         theta = [i[2] for i in self.mpc.data["_x"]]
#         u1 = [i[0] for i in self.mpc.data['_u']]
#         u2 = [i[1] for i in self.mpc.data['_u']]
#
#         time = np.arange(0, len(self.mpc.data["_x"]), 1)
#
#         fig = make_subplots(rows=2, cols=1)
#
#         # reference signal
#         fig.append_trace(go.Scatter(
#             x=[time[0], time[-1]],
#             y=x_ref*np.ones((2,)),
#             name="x_ref",
#             line=dict(color='red', width=1, dash='dash')
#             ), row=1, col=1)
#         fig.append_trace(go.Scatter(
#             x=[time[0], time[-1]],
#             y=y_ref*np.ones((2,)),
#             name="y_ref",
#             line=dict(color='green', width=1, dash='dash')
#             ), row=1, col=1)
#         fig.append_trace(go.Scatter(
#             x=[time[0], time[-1]],
#             y=theta_ref*np.ones((2,)),
#             name="theta_ref",
#             line=dict(color='blue', width=1, dash='dash')
#             ), row=1, col=1)
#
#
#         # x, y and theta positions
#         fig.append_trace(go.Scatter(
#             x=time,
#             y=x,
#             name="x",
#             line=dict(color='red')
#             ), row=1, col=1)
#         fig.append_trace(go.Scatter(
#             x=time,
#             y=y,
#             name="y",
#             line=dict(color='green')
#             ), row=1, col=1)
#         fig.append_trace(go.Scatter(
#             x=time,
#             y=theta,
#             name="theta",
#             line=dict(color='blue')
#             ), row=1, col=1)
#
#
#         fig.append_trace(go.Scatter(
#             x=time,
#             y=u1,
#             name="u1",
#             line=dict(shape='hv')
#         ), row=2, col=1)
#         fig.append_trace(go.Scatter(
#             x=time,
#             y=u2,
#             name="u2",
#             line=dict(shape='hv'),
#         ), row=2, col=1)
#
#         # scale the axis
#         fig.update_xaxes(range=[time[0], time[-1]],
#                          row=1, col=1)
#
#         fig.update_xaxes(range=[time[0], time[-1]],
#                          title_text="Time [sec]",
#                          row=2, col=1)
#
#         fig.update_yaxes(range=[dstack((x, y, theta)).min() - 0.2,
#                                 dstack((x, y, theta)).max() + 0.2],
#                          title_text="position [-]",
#                          row=1, col=1)
#
#         fig.update_yaxes(range=[dstack((u1, u2)).min() - 0.2,
#                                 dstack((u1, u2)).max() + 0.2],
#                          title_text="input [-]",
#                          row=2, col=1)
#
#         fig.update_layout({"title": {"text": "MPC controller"}})
#         
#         fig.update_layout(paper_bgcolor=FIG_BG_COLOR, plot_bgcolor=FIG_BG_COLOR)
#         
#         fig.show()
#         
#          
#         # p_template = simulator.get_p_template()
#         # print(self.mpc.data['_x'])
#         
#         print("this is the shitttt") 
#
#     def visualiseDB(self, dt, current_time):
#         """
#         Stores the MPC data as feather file, for the dashboard
#         """
#
#         dictionary = {
#             "type": "mpc",
#             "x_ref": self.mpc.targetState.pos[0], 
#             "y_ref": self.mpc.targetState.pos[1],
#             "theta_ref": self.mpc.targetState.ang_p[2], # this below should be the mpc.data, not simulatior
#             "x": [i[0] for i in self.simulator.data["_x"]],
#             "y": [i[1] for i in self.simulator.data["_x"]],
#             "theta": [i[2] for i in self.simulator.data["_x"]],
#             "u1": [i[0] for i in self.simulator.data['_u']],
#             "u2": [i[1] for i in self.simulator.data['_u']]
#         }
#
#         # todo: metadata so I can tell this data is mpc data
#         df = pd.DataFrame(dictionary)
#
#         # only store data which will be plotk
#         if current_time >= 15:
#             time = np.arange(current_time-15, current_time, dt)
#             df = df.tail(len(time))
#             df["time"] = time
#         else:
#             df["time"] = np.arange(df.index[0], current_time, dt)
#
#         feather.write_feather(df, '../robot_brain/dashboard/data/mpc_data.feather')
#
#
