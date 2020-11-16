import os
import locale
import datetime

from komapy import Chart
from komapy.conf import settings

locale.setlocale(locale.LC_ALL, 'id_ID')
settings.BMA_API_KEY = os.environ['API_KEY']

# Define global start time and end time
end = datetime.datetime.now()
start = datetime.datetime(2020, 6, 1, 0, 0, 0)
START_TIME = start.strftime('%Y-%m-%d %H:%M:%S')
END_TIME = end.strftime('%Y-%m-%d 08:00:00')

print(START_TIME)
print(END_TIME)


def create_series(benchmark, reflector):
    options = {
        'name': 'edm',
        'query_params': {
            'benchmark': benchmark,
            'reflector': reflector,
            'start_at': START_TIME,
            'end_at': END_TIME,
            'ci': True
        },
        'plot_params': {
            'label': reflector,
            'color': 'k',
            'marker': 'o',
            'markersize': 6,
            'zorder': 2,
            'linewidth': 1,
        },
        'formatter': {
            'y': {
                'major': {
                    'format': '%.3f'
                }
            },
            'x': {
                'major': {
                    'name': 'DateFormatter',
                    'params': ['%b %Y']
                }
            }
        },
        'labels': {
            'y': {
                'text': benchmark
            }
        },
        'legend': {
            'show': True,
            'loc': 'upper left'
        },
        'fields': [
            'timestamp',
            'slope_distance'
        ],
        'xaxis_date': True,
        'locator': {
            'x': {
                'major': {
                    'name': 'MonthLocator'
                }
            },
            'y': {'major': {
                'name': 'LinearLocator',
                'keyword_params': {
                    'numticks': 4
                }
            }},
        },
    }

    return options


def main():
    chart = Chart({
        'title': 'Grafik EDM',
        'rc_params': {
            'font.size': 12,
            'font.sans-serif': ['Helvetica']
        },
        'tight_layout': {
            'pad': 3,
            'w_pad': 0.7,
            'h_pad': 0.5
        },
        'use_cache': True,
        'layout': {
            'options': {
                'sharex': True,
                'figsize': [10, 13]
            },
            'data': [
                {
                    'series': create_series('BAB0', 'RB1')
                },
                {
                    'series': create_series('STA0', 'RB3')
                },
                {
                    'series': create_series('JRK0', 'RJ1')
                },
                {
                    'series': create_series('KAJ0', 'RJ1')
                },
                {
                    'series': create_series('SEL0', 'RS1')
                },
                {
                    'series': create_series('GEB0', 'RS4')
                },
                {
                    'series': create_series('MRY0', 'RM1')
                },
                {
                    'series': create_series('BEL0', 'RM1')
                },
                {
                    'series': create_series('DEL0', 'RD1')
                },
            ]
        },
        'extensions': {
            'starttime': START_TIME,
            'endtime': END_TIME,
            'plot': [
                {
                    'name': 'komapy.extensions.plot_activity_status'
                },
                {
                    'name': 'komapy.extensions.plot_explosion_line',
                    'label': 'Letusan',
                    'color': 'red'
                },
                {
                    'name': 'komapy.extensions.plot_dome_appearance',
                    'label': 'Kubah lava tampak'
                }
            ],
            'legend': {
                'show': True,
                'loc': 'lower center',
                'ncol': 2,
                'frameon': False,
                'fancybox': False
            }
        }
    })

    chart.render()
    chart.save('edm.png')


if __name__ == '__main__':
    main()
