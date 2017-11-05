"""This module is main module for contestant's solution."""

from hackathon.utils.control import Control
from hackathon.utils.utils import ResultsMessage, DataMessage, PVMode, \
    TYPHOON_DIR, config_outs
from hackathon.framework.http_server import prepare_dot_dir


MINS_IN_HOUR = 60
MINS_IN_DAY = 1440

DELTA = 0.1

BATTERY_MAX_POWER = 6.0
BATTERY_MAX_POWER_PER_HOUR = 0.6
BATTERY_MAX_CAPACITY = 1.0

LOAD_MAX_POWER = 8.0
LOAD_DEVIATION = 0.2

L1_POWER_SHARE = 0.2
L2_POWER_SHARE = 0.5
L3_POWER_SHARE = 0.3

L1_LOSS_PENALTY = 20
L2_LOSS_PENALTY = 4
L3_LOSS_PENALTY = 0.0

L1_DOWN_PENALTY = 1
L2_DOWN_PENALTY = 0.4
L3_DOWN_PENALTY = 0.1

POSITIVE_SELLING_PRICE = 3
CHEAP_BUYING_PRICE = 3
EXPENSIVE_BUYING_PRICE = 8

is_previous_load_one_active = True
is_previous_load_two_active = True
is_previous_load_three_active = True
previous_load = 0.0
mins_counter = 0
days_counter = 0


def worker(msg: DataMessage) -> ResultsMessage:
    """TODO: This function should be implemented by contestants."""
    # Details about DataMessage and ResultsMessage objects can be found in /utils/utils.py

    global is_previous_load_one_active
    global is_previous_load_two_active
    global is_previous_load_three_active
    global previous_load
    global mins_counter
    global days_counter

    # Data Message information

    is_buying_price_cheap = msg.buying_price == CHEAP_BUYING_PRICE
    is_selling_price_positive = msg.selling_price == POSITIVE_SELLING_PRICE

    is_grid_status_on = msg.grid_status
    main_grid_power = float(msg.mainGridPower)

    is_battery_overload = msg.bessOverload
    is_battery_full = msg.bessSOC == BATTERY_MAX_CAPACITY


    # pred kraj prodati celu bateriju ?!
    # kupovati bateriju ujutru (izbaci 23 do 24 interval)

    # dodati neku toleranciju za trosenje baterije npr do 0.4, 5

    current_load = msg.current_load

    is_load_rising = current_load > previous_load

    l1 = L1_POWER_SHARE * current_load
    l2 = L2_POWER_SHARE * current_load
    l3 = L3_POWER_SHARE * current_load

    l12 = l1 + l2

    is_battery_prepared_for_electricity_loss = \
        msg.bessSOC * 10 > (l12 if l12 < (BATTERY_MAX_POWER_PER_HOUR + DELTA) * 10 else BATTERY_MAX_POWER_PER_HOUR * 10)

    # 5520 : 0, 8, 3, 9.2, 0, 0.5950260191000842, False, 6.439929503154399
    # 5521, 0, 8, 3, 9.199899290220571, 0, 0.5842926857667509, True, 0

    # 3299, 1, 3, 3, 4.163380970229338, 0, 1.0, False, 2.909085131140325
    # 3300, 1, 8, 3, 4.1708203932499375, 0.0, 1.0, False, 2.9143666791605365

    load_one = True
    power_reference = 0.0

    if not is_grid_status_on:

        load_three = False

        if is_battery_overload:
            load_two = False
            power_reference = l1 - msg.solar_production  # + 0.01
        else:
            load_two = is_previous_load_two_active
            if l12 - msg.solar_production < BATTERY_MAX_POWER + DELTA and not is_load_rising:
                load_two = True
            load_and_solar_diff = (l12 if load_two else l1) - msg.solar_production
            power_reference = load_and_solar_diff if load_and_solar_diff > 0 else 0.0

    else:

        load_three = msg.buying_price * l3 / MINS_IN_HOUR < L3_DOWN_PENALTY
        load_two = True

        if is_buying_price_cheap:

            if not is_battery_full and 1 * MINS_IN_HOUR < mins_counter < 7 * MINS_IN_HOUR:
                power_reference = -BATTERY_MAX_POWER

        else:  # expensive buying

            if l12 > 3.9:
                load_two = False

            if is_battery_prepared_for_electricity_loss:
                load_and_solar_diff = (l12 if load_two else l1) - msg.solar_production
                power_reference = load_and_solar_diff if load_and_solar_diff < BATTERY_MAX_POWER else BATTERY_MAX_POWER

                # else:
                #
                # if is_selling_price_positive and main_grid_power < 0:
                #  power_reference = -main_grid_power  # if main_grid_power > -BATTERY_MAX_POWER else BATTERY_MAX_POWER

    pv_mode = PVMode.ON

    # remember this state for next step

    is_previous_load_one_active = load_one
    is_previous_load_two_active = load_two
    is_previous_load_three_active = load_three
    previous_load = current_load

    if mins_counter < MINS_IN_DAY:
        mins_counter += 1
    else:
        mins_counter = 0
        days_counter += 1

    if days_counter == 4 and mins_counter > 1398:
        power_reference = BATTERY_MAX_POWER

    return ResultsMessage(data_msg=msg,
                          load_one=load_one,
                          load_two=load_two,
                          load_three=load_three,
                          power_reference=power_reference,
                          pv_mode=pv_mode)


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
            resp.load_three = False
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

