import os

from komapy import Chart
from komapy.conf import settings

settings.BMA_API_KEY = os.environ['API_KEY']

chart = Chart({
    'title': 'Grafik EDM RB2',
    'use_cache': True,
    'tight_layout': {
        'pad': 2.5,
    },
    'rc_params': {
        'font.size': 11,
        'font.sans-serif': ['Helvetica']
    },
    'layout': {
        'options': {
            'figsize': [14, 6],
        },
        'data': [
            {
                'series': {
                    'partial': [
                        {
                            'name': 'edm',
                            'query_params': {
                                'timestamp__gte': '2014-01-01',
                                'timestamp__lt': '2019-03-01',
                                'benchmark': 'BAB0',
                                'reflector': 'RB2',
                                'nolimit': True,
                            }
                        },
                        {
                            'name': 'edm',
                            'query_params': {
                                'start_at': '2019-03-01',
                                'end_at': '2020-05-01',
                                'benchmark': 'BAB0',
                                'reflector': 'RB2',
                                'ci': True,
                            }
                        },
                    ],
                    'xaxis_date': True,
                    'plot_params': {
                        'label': 'RB2',
                        'color': 'k',
                        'marker': 'o',
                        'markersize': 6,
                        'zorder': 2,
                        'linewidth': 1,
                    },
                    'fields': ['timestamp', 'slope_distance'],
                    'formatter': {
                        'y': {
                            'major': {
                                'format': '%.3f'
                            }
                        },
                        'x': {
                            'major': {
                                'name': 'DateFormatter',
                                'params': ['%Y']
                            },
                        }
                    },
                    'locator': {
                        'y': {
                            'major': {
                                'name': 'LinearLocator',
                                'keyword_params': {
                                    'numticks': 8
                                }
                            },
                            'minor': {
                                'name': 'AutoMinorLocator',
                            }
                        },
                        'x': {
                            'minor': {
                                'name': 'MonthLocator',
                            },
                            'major': {
                                'name': 'YearLocator',
                            }
                        }
                    },
                    'labels': {
                        'y': {
                            'text': 'Jarak miring (m)'
                        }
                    },
                    'legend': {
                        'show': True,
                        'loc': 'upper left'
                    },
                }
            }
        ]
    },
    'extensions': {
        'starttime': '2014-01-01',
        'endtime': '2020-05-01',
        'plot': [
            {
                'name': 'komapy.extensions.activity_status',
            },
            {
                'name': 'komapy.extensions.explosion',
                'label': 'Letusan',
                'color': 'red'
            },
            {
                'name': 'komapy.extensions.dome',
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
    },
})

chart.render()
chart.save('edm.png')
