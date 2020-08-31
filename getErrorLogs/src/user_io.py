import os

from datetime import datetime
from glob import glob

def get_datetime(app):
    to_datetime = datetime.now()
    from_datetime = get_from_datetime(app)

    return (from_datetime, to_datetime)

def get_from_datetime(app):
    base_URL="../data/" + app
    file_paths = glob(base_URL+"/*.log")
    file_names = [os.path.split(fpath)[-1] for fpath in file_paths]
    
    datetimes = [f_t[:-4] for f_t in file_names]
    to_datetimes = [datetime.split("-")[-1] for datetime in datetimes]
    to_datetimes = [datetime.strptime(d, '%Y%m%d%H%M%S') for d in to_datetimes]

    # latest_to_datetime = next from_datetime
    from_datetime = max(to_datetimes)

    return from_datetime
