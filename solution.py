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
    """
    When buying price is 8 (max), turn off load three
    """
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

def logic2(func):
    """
    When buying price is 8 (max), turn off load three
    """
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

def logic3(func):
    """
    When buying price is 8 (max), turn off load three
    """
    def func_wrapper(msg):
        resp = func(msg)
        # TODO: Import your logic here
        return resp
    return func_wrapper

def logic4(func):
    """
    When buying price is 8 (max), turn off load three
    """
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



