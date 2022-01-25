from pprint import pprint

from Loading.calc_metrics import states


def get_info(state: str):
    # print()
    result = states.find_one({'NAME': state})
    del result['Counties']
    del result['_id']
    pprint(result)
