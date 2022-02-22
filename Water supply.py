"""
Automation of hydraulic calculations of the project of providing clean water to the countryside.
It is assumed that clean water will be drawn from wells and distributed to the region.
author: @FurkanEmiroglu
"""
import numpy as np
import math
import population
import regulation


def ask_data():
    """
    This function asks for data required listed below.

    Returns:
        diameter (float):  Diameter of the well to be drilled for getting water.
        k_coeff (float): Manning coefficient 
        H (float): Well Depth
        well_altitude: Altitude of the well relative to the sea level.
    """
    diameter = int(input())
    k_coeff = int(input()) / 100
    H_coeff = int(input())
    well_altitude = int(input())
    return diameter, k_coeff, H_coeff, well_altitude


def main_flow(future_pop, wastewaterdaily, fire_dept, diameter):
    """
    Args:
        future_pop (int): The population predicted when the project is at the end of its lifespan.
        wastewaterdaily (int): Daily waste water production amount, determined by the regulation.
        diameter (float): Diameter of the well that will be the source of water.

    Returns:
        main_flow_rate (float): flow rate in the main pipe of water supplying system. (cubic meter/second)

    """
    city_water_needs = future_pop * wastewaterdaily / 86400
    industrial_needs = diameter * city_water_needs
    safety_coeff = 1.5
    main_flow_rate = (
        # . . the unit of the main flow is liters/second
        safety_coeff * (city_water_needs + industrial_needs) + fire_dept)

    # . . converting main flow rate to cubicmeter/second
    main_flow_rate = main_flow_rate / 100

    # . . calculating flow rate that will pass through the main line regularly
    transmitted_flow = city_water_needs + industrial_needs

    # . . printing out results
    print(
        f"for values future pop: {future_pop},  wastewaterdaily: {wastewaterdaily}, " +
        f" fire dept: {fire_dept}  diameter: {diameter} our expected main flow is " +
        f" {main_flow_rate} cubicmeter/second")

    # . . returning results
    return main_flow_rate, transmitted_flow


def well_sec_check(diameter, H, k, iterations):
    """
    Solves an equation to find security coefficient S which is important for renewability calculations.

    Args:
        diameter (float): diameter of the well that will be the source of water. (meter)
        H (float): 
        k (float):
        Iterations (int): number of iterations to solve the equation.

    Returns:
        S_sec (float): security coefficient for max amount of descent tolerable for continuous use of the well.
        Q_cr (float): critical amount of flow that must not be exceeded for continuous use. (cubicmeter/second)
        Q_sec (float): critical amount of flow that must not be exceeded for safe descent to occur.

    Note:
        Q_cr and Q_sec must be equal to continue.
        """
    S_sec = 0.01
    equation = 0
    for i in range(iterations):
        equation = (2 * diameter) * (H - S_sec) / (15 * (k)**(0.5)) / \
            (2 * H - S_sec) * np.log((3000 * S_sec * (k)**(0.5) / diameter))
        S_sec += 0.01
        if (round(S_sec, 2) == round(equation, 2)):
            break
        else:
            continue
    S_sec = round(S_sec, 2)

    # . . printing S_sec
    print(f"S_sec is: {S_sec}")

    return S_sec


def flow_sec_check(diameter, H, k, S_sec):
    """
    Calculates decision boundary (critical point for flow rate in the main pipe. Our main flow should stay under the Q_sec for
    continuous use of the well.

    Args:
        diameter (float): diameter of the well that will be the source of water (meter)
        H (float): 
        k_coeff (float):
        S_sec (float): calculated S_sec coefficient from well_sec_check.

    Returns:
        Q_sec (float): critical point indicating the amount of flow that the current should not exceed. (cubicmeter/second)
    """
    Q_sec = np.pi * k * S_sec * \
        (2 * H - S_sec) / np.log(3000 * np.sqrt(k) / diameter * S_sec)
    Q_sec = round(Q_sec, 3)
    descent = round((H - S_sec), 3)
    Q_cr = round((2 * np.pi * diameter * descent * np.sqrt(k) / 15), 3)
    if Q_sec == Q_cr:
        print(f"Q_sec = Q_cr check achieved and they are both {Q_sec}")
        return Q_sec
    else:
        print(
            f"Q_sec = Q_cr check failed. Q_sec is {Q_sec}, Q_cr is {Q_cr}")


def compare_real_descent(diameter, main_flow_rate, Q_sec, S_sec, H, k, iterations):
    """
    It compares the amount of descent that will occur with the amount of descent that will be created by the critical flow.

    Args:
        diameter (float): diameter of the well that will be the source of water (meter)
        main_flow_rate (float): flow rate in the main pipe. (cubicmeter/second)
        Q_sec (float): critical point indicating the amount of flow that the current should not exceed. (cubicmeter/second)
        S_sec (float): calculated S_sec coefficient from well_sec_check.
        H (float):
        k (float):
        iterations (int): amount of iteration to converge to the solution.

    Returns:
        S_real (float): amount of descent will occur in the well.
        descent_equation (float): 
    """
    # . . calculating number of wells needed.
    n_well = main_flow_rate / (Q_sec * 1000)
    n_well = math.ceil(n_well)

    # Calculating flow per pipe. (cubic meter / second)
    flow_pp = main_flow_rate / n_well

    # Calculating actual descent in the well
    S_real = 0.01
    for i in range(iterations):
        descent_equation = flow_pp / \
            (np.pi * k) / (2 * H - S_real) * \
            np.log(3000 * S_real * (np.sqrt(k)) / diameter)
        if round(S_real, 2) == round(descent_equation, 2):
            S_real = round(S_real, 2)
            print(
                f"Success: Amount of descent is within safe limits. S_real: {S_real} ")
            break
        elif round(S_real, 2) > round(S_sec, 2):
            S_real = round(S_real, 2)
            print(
                f"Failure: Amount of descent IS NOT TOLERABLE! S_real: {S_real} ")
            break
        else:
            S_real += 0.01
            continue
    descent_equation = round(descent_equation, 2)
    return S_real


def reservoir_design(transmitted_flow, fire_dept):
    """
    Performs the sizing of the city's water reservoir.

    Args:
        main_flow_rate (float): flow rate in the main pipe. (cubicmeter/second)
        fire_dept (float): amount of water to be allocated to fire departments. (cubicmeter/second)

    Returns:
        Lx (float): the length of the water reservoir in the x direction. (meter)
        Ly (float): the lenght of the water reservoir in the y direction. (meter)
    """
    # . . calculating consumption per second
    volume_daily = transmitted_flow * 86400 / 1000

    # . . this is due to legal regulations
    active_usage = volume_daily / 4

    # . . calculating minimum reservoir volume
    reservoir_min = active_usage + fire_dept
    reservoir = ((lambda x: int(math.ceil(x / 250)) * 250)(reservoir_min))

    # . . reading the legally expected water height in the reservoir
    height = regulation.water_height(reservoir)

    # . . determination of reservoir dimensions
    a = np.sqrt(reservoir / (24*height))

    # Rounding up the coefficient
    a = math.ceil(a * 100) / 100

    # . . the ratio of the edges to each other must be around 3:4 for minimum energy loss
    Lx = round((math.ceil(3*a * 100) / 100), 1)
    Ly = round((math.ceil(4*a * 100) / 100), 1)

    # . . printing out results
    print(f"Transmitted flow rate is: {transmitted_flow} liter/second")
    print(f"Reservoir volume is {reservoir}")
    print(
        f"Designed reservoir dimensions: \r\n {Lx} meters width \r\n {Ly} meters lenght")

    return Lx, Ly


def economical_pipe_diameter(main_flow_rate):
    """
    Calculates the economical diameter for the main pipe, taking into account the energy losses.

    Args:
        main_flow_rate (float): flow rate in the main pipe. (cubicmeter/second)

    Returns:
        pipe_diameter (float): pipe diameter minimizing energy loss. (milimeter)
    """
    # . . defining frequently used pipe diameters
    pipe_list = np.arange(0.1, 0.525, 0.025)

    # . . for minimal energy loss velocity must be around 1 meter/second
    # . . trying out different pipe diameters for optimum result
    for pipe_diameter in pipe_list:
        velocity = 4 * (main_flow_rate/(np.pi*np.square(pipe_diameter)))
        if velocity >= 0.9 and velocity <= 1.1:
            pipe_diameter = round(pipe_diameter, 3)
            print(
                f"Economical pipe diameter selected for water supply: {pipe_diameter}")
            return pipe_diameter
        else:
            continue
        print(
            "Flow is intolerable, couldn't find a pipe diameter for minmized energy loss.")


def run():
    # ask_data()
    first_measurement = population.measurement(1990, 16439)
    second_measurement = population.measurement(2015, 23380)
    building_year = 2030
    project_lifetime = 35
    diameter = 0.2
    H_coeff = 42.2
    k_coeff = 0.00068
    iterations = 1500
    # -------------------- #
    # . . outputting growth rate
    growth_rate = population.growth_rate(first_measurement, second_measurement)

    # . . calculating future population at the end-of-service time of project
    future_pop = population.estimator(
        second_measurement, building_year, project_lifetime, growth_rate)

    # . . calculating daily wastewater production
    wastewaterdaily = regulation.wastewater(future_pop)

    # . . reading the water flow requirement for fire disasters in the regulation
    fire_dept = regulation.fire_dept_need(future_pop)

    # . . calculating main flow rate
    main_flow_rate, transmitted_flow = main_flow(
        future_pop, wastewaterdaily, fire_dept, diameter)

    # . . control of renewability principles
    S_sec = well_sec_check(diameter, H_coeff, k_coeff, iterations)

    # . . calculating for critical flow rate
    Q_sec = flow_sec_check(diameter, H_coeff, k_coeff, S_sec)

    # . . comparing real descent in the well vs. critical descent for renewability
    S_real = compare_real_descent(
        diameter, transmitted_flow/1000, Q_sec, S_sec, H_coeff, k_coeff, iterations)

    # . . designing the reservoir
    Lx, Ly = reservoir_design(transmitted_flow, fire_dept)

    # . . calculating pipe diameter for tolerable energy loss
    pipe_diam = economical_pipe_diameter(transmitted_flow/1000)


run()
