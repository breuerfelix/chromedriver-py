import os
import platform

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_bit(last = None):
    if last and last == '64': return '32'
    if last and last == '32': return '64'

    if platform.machine().endswith('64'): return '64'
    
    return '32'



def _get_filename(last_bit = None):
    path = os.path.join(_BASE_DIR, 'chromedriver_')

    sys = platform.system()
    if sys == 'Windows':
        path += 'win'
    elif sys == 'Darwin':
        path += 'mac'
    elif sys == 'Linux':
        path += 'linux'
    else:
        raise Exception('could not identify your system!')

    bit = _get_bit(last_bit)
    path += bit

    if sys == 'Windows':
        path += '.exe'

    exists = os.path.isfile(path)

    if not exists and not last_bit:
        path = _get_filename(bit)

    if not path:
        raise Exception('error getting your chromedriver version')

    return path



binary_path = _get_filename()
