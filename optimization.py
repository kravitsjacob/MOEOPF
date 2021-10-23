
# Import Packages
import numpy as np
import pandas as pd
import os
import pandapower as pp
import pandapower.networks
from borg import *


# Global Vars
pathto_data = 'MOEOPF_io'
pathto_generator_limits = os.path.join(pathto_data, 'Input', 'generator_limits.csv')
pathto_cost_coef = os.path.join(pathto_data, 'Input', 'costs.csv')
pathto_emit_coef = os.path.join(pathto_data, 'Input', 'emissions.csv')
pathto_bus_limits = os.path.join(pathto_data, 'Input', 'bus_limits.csv')
pathto_runtime = os.path.join(pathto_data, 'Output', 'runtime.txt')
pathto_results = os.path.join(pathto_data, 'Output', 'results.csv')


def solve_power_flow(*vars):
    """
    Solve for the power at generator 1 such that the powerflow equations are satisfied
    @param vars: tuple: Activate Power for Generators 2-5 in MW
    @return: DataFrames: Generator power outputs and bus voltages
    """
    # Initialize Vars
    gen_names = ['G_1', 'G_2', 'G_3', 'G_4', 'G_5', 'G_6']
    # Import the Network
    net = pandapower.networks.case_ieee30()
    # Map Decisions
    net.gen['p_mw'] = vars
    # Solve the Powerflow Equations
    pp.runpp(net, init="flat", numba=False, enforce_q_lims=False, calculate_voltage_angles=True)
    # Extract Generators
    gen_df = pd.DataFrame({'p_mw': net.res_gen['p_mw'].to_list() + net.res_ext_grid['p_mw'].to_list()}, index=gen_names)
    bus_df = pd.DataFrame(net.res_bus['vm_pu'])
    # Export
    return gen_df, bus_df


def get_gen_constraint(df):
    """
    Get generator power constraint value
    @param df: DataFrame: Generator power outputs
    @return: float: constraint value (anything other than 0.0 is an infeasible set of generator values)
    """
    # Initialize Vars
    cons = 0.0
    # Import Generation Lim
    lim = pd.read_csv(pathto_generator_limits, index_col=0)
    # Exceeds Maximum Capacity
    cons = cons + float(sum(x for x in df['p_mw']/100 - lim['max'] if x > 0))  # Unit Power
    cons = cons + float(abs(sum(x for x in df['p_mw']/100 - lim['min'] if x < 0)))
    # Export
    return cons


def get_cost(df):
    """
    Get fuel cost of current set of generators
    @param df: DataFrame: Generator power outputs
    @return: float: Fuel cost of current set of generators
    """
    # Initialize Vars
    obj = 0.0
    # Import Cost Coefficients
    cost_df = pd.read_csv(pathto_cost_coef, index_col=0)
    # Compute Cost
    term1 = cost_df['a']
    term2 = cost_df['b'] * (df['p_mw']/100)
    term3 = cost_df['c'] * (df['p_mw']/100)**2
    obj = obj + np.sum(term1 + term2 + term3)
    # Export
    return obj


def get_emission(df):
    """
    Get emission value of current set of generators
    @param df: DataFrame: Generator power outputs
    @return: float: Emission value of current set of generators
    """
    # Initialize Vars
    obj = 0.0
    # Import Emissions Coefficients
    emit_df = pd.read_csv(pathto_emit_coef, index_col=0)
    # Compute Emissions
    term1 = 0.01 * emit_df['alpha']
    term2 = 0.01 * emit_df['beta'] * (df['p_mw']/100)
    term3 = 0.01 * emit_df['gamma'] * (df['p_mw']/100)**2
    term4 = emit_df['xi'] * np.exp(emit_df['lambda'] * (df['p_mw']/100))
    obj = obj + np.sum(term1 + term2 + term3 + term4)
    # Export
    return obj


def get_system_voltage_violation(df):
    """
    Get sum of system-wide voltage violations
    @param df: DataFrame: Bus voltages
    @return: float: sum of system-wide voltage violations
    """
    # Initialize Vars
    obj = 0.0
    # Import Emissions Coefficients
    emit_df = pd.read_csv(os.path.join(pathto_bus_limits), index_col=0)
    # Exceeds Voltage Limits
    obj = obj + float(sum(x for x in df['vm_pu'] - emit_df['max'] if x > 0))
    obj = obj + float(abs(sum(x for x in df['vm_pu'] - emit_df['min'] if x < 0)))
    return obj


def simulation(*vars):
    """
    Evaluate a set of generator power levels
    @param vars: Generator power levels for generators 2-5
    @return: floats: objective and constraint values
    """
    gen_df, bus_df = solve_power_flow(*vars)
    # Compute Constraint
    generation_con = get_gen_constraint(gen_df)
    # Compute Objectives
    cost_obj = get_cost(gen_df)
    emit_obj = get_emission(gen_df)
    system_volt_obj = get_system_voltage_violation(bus_df)
    # Format Results
    objs = [cost_obj, emit_obj, system_volt_obj]
    cons = [generation_con]
    print(vars)
    print(objs)
    print(cons)
    print(gen_df)
    # Export
    return objs, cons


def main():
    # Problem setup
    Configuration.seed(1008)
    borg = Borg(numberOfVariables=5, numberOfObjectives=3, numberOfConstraints=1, function=simulation)
    borg.setBounds((5, 150), (5, 150), (5, 150), (5, 150), (5, 150))
    borg.setEpsilons(0.1, 0.0001, 0.0001)
    print('Success: Setup Optimization')
    # Run Optimization
    result = borg.solve(
        {'maxEvaluations': 20000,
         'initialPopulationSize': 100,
         'runtimeformat': 'borg',
         'frequency': 1000, 'runtimefile': pathto_runtime}
    )
    print('Success: Run Optimization')
    return 0


if __name__ == '__main__':
    main()
