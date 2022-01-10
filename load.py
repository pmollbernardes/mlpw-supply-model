import sys
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

date_parse = lambda dates: [datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p') for d in dates]

def load_daily_generation_data(input_file):
    records = pd.read_csv(input_file, parse_dates=['datetime_beginning_ept', 'datetime_beginning_utc'], date_parser=date_parse).to_dict('records')
    records = list(reversed(records))
    current_day = None
    timestamps = []
    renewables = []
    non_renewables = []
    wind = []
    coal = []
    total = []
    for entry in records:
        timestamp = entry['datetime_beginning_utc']
        if timestamp.day != current_day:
            timestamps.append(timestamp)
            wind.append(0)
            coal.append(0)
            renewables.append(0)
            non_renewables.append(0)
            total.append(0)
        current_day = timestamp.day
        if entry['fuel_type'] == 'Wind':
            wind[-1] += entry['mw']
        if entry['fuel_type'] == 'Coal':
            coal[-1] += entry['mw']
        if entry['is_renewable']:
            renewables[-1] += entry['mw']
        else:
            non_renewables[-1] += entry['mw']
        total[-1] += entry['mw']
    #Remove first and last (incomplete) days
    for series in [timestamps, renewables, non_renewables, wind, coal, total]:
        del series[0]
        del series[-1]
    return {
        'wind': wind,
        'coal': coal,
        'renewables': renewables,
        'non_renewables': non_renewables,
        'total': total,
        'timestamps': timestamps
    }

if __name__ == '__main__':
    input_file = sys.argv[1]
    data = load_daily_generation_data(input_file)
    print(len(data['timestamps']))
    plt.plot(data['timestamps'], data['non_renewables'])
    plt.show()
