"""
This script uses statistical methods to estimate the population that will benefit from the water supply system
throughout the life of the project.
author: @FurkanEmiroglu
"""

from math import ceil


class measurement:
    """
    This object stores the survey containing the population measurement results for any given year.
    We'll use our results for estimating future population.
    """

    def __init__(self, year, result):
        self.year = year
        self.result = result


def growth_rate(first, second):
    """
    Calculates the rate of increase by examining two different population measurements.
    Args:
        first (measurement): Population data for the first measurement we have.
        second (measurement): Population data for the second measurement we have.
    Returns:
        p (float): Population growth rate.
    """

    try:
        # checking the year order
        assert first.year < second.year
        # calculating the population growth rate.
        p = 100 * ((second.result / first.result) **
                   (1 / (second.year - first.year)) - 1)
        # implementing statistical limitations.
        if p >= 3:
            p = 3
            print(f"Our growth rate is {p}")
            return p
        else:
            p = round(p, 3)
            print(f"Our growth rate is {p}")
            return p
    except:
        raise AssertionError(
            "First measurement year is after the second measurement year.")


def estimator(last_measurement, building_year, project_lifetime, growth_rate):
    """
    Estimates the population the area will have at the end of the project service life.
    Args:
        last_measurement (measurement): Population data for the second measurement we have.
        building_year (int): The year in which the construction is expected to be completed and put into service.
        project_lifetime (int): Planned service life of the water supply system.
        growth_rate (float): A coefficient used in the predicting the future population process. 
            Calculated in the growth_rate function.
    Returns:
        expected_population (int): The expected population of the area at the end of the project service life.
    """
    n = building_year - last_measurement.year + project_lifetime
    expected_population = (1+(growth_rate/100))**(n) * last_measurement.result
    expected_population = ceil(expected_population)
    print(
        f"Estimated population at project end-of-life: {expected_population}")
    return expected_population
