import os

from komapy import Chart

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rb2.csv')

chart = Chart({
    'title': 'Grafik EDM RB2',
    'rc_params': {
        'font.size': 11,
        'font.sans-serif': ['Helvetica']
    },
    'layout': {
        'options': {
            'figsize': [12, 4],
        },
        'data': [
            {
                'series': {
                    'csv': CSV_PATH,
                    'csv_params': {
                        'delimiter': ',',
                        'header': 0,
                    },
                    'fields': ['timestamp', 'slope_distance'],
                    'xaxis_date': True,
                    'plot_params': {
                        'label': 'RB2',
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
                            'text': 'Jarak miring (m)'
                        }
                    },
                    'locator': {
                        'y': {
                            'major': {
                                'name': 'LinearLocator',
                                'keyword_params': {
                                    'numticks': 7
                                }
                            },
                            'minor': {
                                'name': 'AutoMinorLocator',
                            }
                        },
                        'x': {
                            'minor': {
                                'name': 'DayLocator',
                            }
                        }
                    },
                    'addons': [
                        {
                            'name': 'komapy.addons.set_axis_xlimit',
                            'value': ['2019-12-25', '2020-07-10'],
                            'datetime': True,
                        }
                    ]
                }
            }
        ]
    }
})

chart.render()
chart.save('rb2.png')

