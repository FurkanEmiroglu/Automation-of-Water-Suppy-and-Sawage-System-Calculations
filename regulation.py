"""
This script has been prepared for the compliance checks of the quality standards determined by the Turkish government.
Author: @FurkanEmiroglu
"""


def wastewater(population):
    """
    Legal directive on population and daily water consumption.
    Args:
        population (int, optional): Population of the region.
    Returns:
        wastewater (int): Per capita daily water consumption prescribed by law.
    """
    if population < 3000:
        wastewater = 60
        return wastewater
    elif population in range(3000, 5001):
        wastewater = 70
        return wastewater
    elif population in range(5001, 10000):
        wastewater = 80
        return wastewater
    elif population in range(10001, 30000):
        wastewater = 100
        return wastewater
    elif population in range(30001, 50000):
        wastewater = 120
        return wastewater
    elif population in range(50001, 100000):
        wastewater = 170
        return wastewater
    elif population in range(100001, 200000):
        wastewater = 200
        return wastewater
    elif population in range(200001, 300000):
        wastewater = 225
        return wastewater
    elif population >= 300000:
        wastewater = 250
        return wastewater


def water_height(reservoir):
    """
    Legally required water height in the city water reservoir, depending on the reservoir volume.
    Args:
        reservoir (int): The volume of the city reservoir.
    Returns:
        height (int): Demanded height of water in the reservoir.
    """
    # . .
    if reservoir in range(0, 300):
        height = 3
        return height
    elif reservoir in range(300, 500):
        height = 3.5
        return height
    elif reservoir in range(500, 900):
        height = 4
        return height
    elif reservoir in range(900, 2000):
        height = 5
        return height
    elif reservoir >= 2000:
        height = 6
        return height


def fire_dept_need(population):
    """
    Water flow rate determined by law, which must be allocated to fire services.
    Args:
        population (int): Population of the region.
    Returns:
        fire_dept (int): Flow rate to be allocated to the fire service. (cubicmeter/second)
    """
    population = round(population, 0)
    if population in range(10000):
        fire_dept = 10
        return fire_dept
    elif population in range(10000, 25000):
        fire_dept = 15
        return fire_dept
    elif population in range(25000, 100000):
        # . . this number is actually 20 but it will stay 10 for testing a bug.
        # fire_dept = 20
        fire_dept = 10
        return fire_dept
    elif population > 100000:
        fire_dept = 25
        return fire_dept
