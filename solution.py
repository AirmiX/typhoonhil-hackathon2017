"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py
    res = get_result(msg)
    return res


def run(args) -> None:
    prepare_dot_dir()
    config_outs(args, 'solution')

    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))


###
### Logic decorators
###

def expencive_grid(func):
    """
    When buying price is 8 (max), turn off load three
    """
    def func_wrapper(msg):
        resp = func(msg)
        if msg.buying_price == 8:
            resp.load_three=False
        return resp
    return func_wrapper


def logic1(func):
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

def logic2(func):
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

def logic3(func):
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

def logic4(func):
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

###
### Logic decorators end
###

# Add your logics
@expencive_grid
@logic1
@logic2
@logic3
@logic4
def get_result(msg):
    return ResultsMessage(data_msg=msg,
                          load_one=True,
                          load_two=True,
                          load_three=True,
                          power_reference=0.0,
                          pv_mode=PVMode.ON)



###

# DELTA = 0.4

# BATTERY_MAX_POWER = 6.0
# BATTERY_MAX_POWER_PER_HOUR = 0.6

# LOAD_MAX_POWER = 8.0
# LOAD_DEVIATION = 0.2
# LOAD_ONE_POWER_SHARE = 0.2
# LOAD_TWO_POWER_SHARE = 0.5
# LOAD_THREE_POWER_SHARE = 0.3

# POSITIVE_SELLING_PRICE = 3
# CHEAP_BUYING_PRICE = 3
# EXPENSIVE_BUYING_PRICE = 8


# def worker(msg: DataMessage) -> ResultsMessage:
#     """TODO: This function should be implemented by contestants."""
#     # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

#     # Data Message information

#     is_buying_price_cheap = msg.buying_price == CHEAP_BUYING_PRICE
#     is_selling_price_positive = msg.selling_price == POSITIVE_SELLING_PRICE

#     is_grid_status_on = msg.grid_status
#     load_and_solar_diff = float(msg.current_load - msg.solar_production)
#     main_grid_power = float(msg.mainGridPower)

#     is_battery_overload = msg.bessOverload
#     is_buttery_prepared_for_electricity_loss = msg.bessSOC > BATTERY_MAX_POWER_PER_HOUR

#     #

#     load_one = True

#     load_three = is_buying_price_cheap and is_grid_status_on is True

#     power_reference = 0.0

#     if msg.grid_status is False:

# # 20 posto od celog koliko je ako samo rade one and two
#         load_two = msg.current_load * (1 - LOAD_TWO_POWER_SHARE) < BATTERY_MAX_POWER - DELTA

#         power_reference = load_and_solar_diff

#     else:

#         load_two = True

#         if is_buttery_prepared_for_electricity_loss:

#             if not is_buying_price_cheap:
#                 power_reference = load_and_solar_diff if load_and_solar_diff < 6 else BATTERY_MAX_POWER

#             # else:
#             #
#             #     if is_selling_price_positive and msg.mainGridPower < 0:
#             #         power_reference = -main_grid_power  # if msg.mainGridPower > -6 else 6

#         else:

#             if is_buying_price_cheap:
#                 power_reference = -6.0

#     pv_mode = PVMode.ON

#     return ResultsMessage(data_msg=msg,
#                           load_one=load_one,
#                           load_two=load_two,
#                           load_three=load_three,
#                           power_reference=power_reference,
#                           pv_mode=pv_mode)



