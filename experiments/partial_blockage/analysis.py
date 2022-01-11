import json
import time
from math import ceil
from random import seed

from agents.fixed_velocity_agent import FixedVelocityAgent
from planners.full_blockage.separate_traveling_planner import SeparateTravelingPlanner
from planners.full_blockage.static_line_planner import StaticLinePlanner
from planners.full_blockage.traveling_line_planner import TravelingLinePlanner
from planners.greedy.kmeans_assignment_planner import KmeansAssignmentPlanner
from planners.greedy.iterative_assignment_planner import IterativeAssignmentPlanner
from planners.planner import Planner
from utils.functions import *

with open('./config.json') as json_file:
    config = json.load(json_file)


def run(planner: Planner):
    agents = [FixedVelocityAgent(sample_point(config['x_buffer'], config['x_buffer'] + config['x_size'],
                                              config['y_buffer'], config['y_buffer'] + config['y_size_init']),
                                 config['agent_speed']) for _ in range(config['num_agents'])]

    robots = [BasicRobot(sample_point(0, config['x_size'] + 2 * config['x_buffer'], 0, config['y_buffer']),
                         config['robot_speed'], config['disablement_range'], has_mode=True)
              for _ in range(config['num_robots'])]

    env = Environment(agents=agents, robots=robots, border=config['y_size'] + config['y_buffer'])

    before = time.time()
    movement, active_time, expected_damage, expected_num_disabled = planner.plan(env)
    planning_time = time.time() - before

    write_report(planner=str(planner),
                 num_agents=config['num_agents'],
                 num_robots=config['num_robots'],
                 f=config['robot_speed'] / config['agent_speed'],
                 d=config['disablement_range'],
                 active_time=active_time,
                 planner_time=planning_time,
                 damage=expected_damage,
                 num_disabled=expected_num_disabled,
                 file_name='../full_blockage/past/agents_results.csv')


if __name__ == '__main__':
    planners = [TravelingLinePlanner(),
                IterativeAssignmentPlanner(),
                KmeansAssignmentPlanner(),
                SeparateTravelingPlanner(),
                TravelingLinePlanner()]

    for planner in planners:
        for v in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            for s in range(30):
                seed(s)

                config['num_agents'] = v
                print(f'running {str(planner)} ..')
                run(planner)