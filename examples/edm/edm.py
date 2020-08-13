import os
import locale

from komapy import Chart
from komapy.conf import settings

locale.setlocale(locale.LC_ALL, 'id_ID')
settings.BMA_API_KEY = os.environ['API_KEY']

# Define global start time and end time
START_TIME = '2020-01-01'
END_TIME = '2020-07-01'


def create_series(benchmark, reflector):
    return {
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
        'xaxis_date': True
    }


def main():
    chart = Chart({
        'title': 'Grafik EDM',
        'rc_params': {
            'font.size': 11,
            'font.sans-serif': ['Helvetica']
        },
        'tight_layout': {
            'pad': 3,
            'w_pad': 0.5,
            'h_pad': 0.7
        },
        'use_cache': True,
        'layout': {
            'options': {
                'sharex': True,
                'figsize': [10, 9]
            },
            'data': [
                {
                    'series': create_series('BAB0', 'RB1')
                },
                {
                    'series': create_series('DEL0', 'RD1')
                },
                {
                    'series': create_series('JRK0', 'RJ1')
                },
                {
                    'series': create_series('KAL0', 'RK2')
                },
                {
                    'series': create_series('MRY0', 'RM1')
                },
                {
                    'series': create_series('SEL0', 'RS1')
                },
                {
                    'series': create_series('STA0', 'RB3')
                },
            ]
        },
        'extensions': {
            'starttime': START_TIME,
            'endtime': END_TIME,
            'plot': [
                {
                    'name': 'komapy.extensions.plot_activity_status'
                }
            ]
        }
    })

    chart.render()
    chart.save('edm.png')


if __name__ == '__main__':
    main()
