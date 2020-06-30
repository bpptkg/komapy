from komapy import Chart
from komapy.client import set_api_key
from komapy.extensions import register_extension

set_api_key('YOUR_API_KEY')


def config_factory(*args, **kwargs):
    starttime = kwargs['starttime']
    endtime = kwargs['endtime']

    config = {
        'tight_layout': {
            'pad': 3,
            'w_pad': 0.5,
            'h_pad': 0.6
        },
        'use_cache': True,
        'rc_params': {
            'font.size': 12,
            'font.sans-serif': ['Helvetica']
        },
        'layout': {
            'options': {
                'sharex': True,
                'figsize': [12, 6]
            },
            'data': [
                {
                    'series': [
                        {
                            'name': 'gas_emission',
                            'query_params': {
                                'timestamp__gte': starttime,
                                'timestamp__lt': endtime,
                                'nolimit': True,
                            },
                            'plot_params': {
                                'linewidth': 1,
                                'label': 'CO$_2$ maks.',
                                'color': 'blue'
                            },
                            'fields': ['timestamp', 'co2_max'],
                            'xaxis_date': True,
                            'formatter': {
                                'y': {
                                    'major': {
                                        'format': '%.1f'
                                    }
                                },
                                'x': {
                                    'major': {
                                        'name': 'ConciseDateFormatter',
                                    }
                                }
                            },
                            'locator': {
                                'y': {
                                    'major': {
                                        'name': 'MaxNLocator',
                                        'params': [7]
                                    }
                                },
                                'x': {
                                    'major': {
                                        'name': 'AutoDateLocator'
                                    }
                                }
                            },
                            'labels': {
                                'y': {
                                    'text': 'Konsentrasi CO$_2$ (ppm)'
                                }
                            },
                        },

                        {
                            'name': 'gas_temperature',
                            'query_params': {
                                'timestamp__gte': starttime,
                                'timestamp__lt': endtime,
                                'nolimit': True,
                            },
                            'plot_params': {
                                'linewidth': 1,
                                'label': 'Suhu tanah',
                                'color': 'orange'
                            },
                            'fields': ['timestamp', 'temperature1'],
                            'xaxis_date': True,
                            'secondary': 'x',
                            'formatter': {
                                'y': {
                                    'major': {
                                        'format': '%.1f'
                                    }
                                }
                            },
                            'locator': {
                                'y': {
                                    'major': {
                                        'name': 'MaxNLocator',
                                        'params': [7]
                                    }
                                }
                            },
                            'labels': {
                                'y': {
                                    'text': r'Suhu tanah & termokopel ($^\circ$C)'
                                }
                            },
                        },

                        {
                            'name': 'gas_temperature',
                            'query_params': {
                                'timestamp__gte': starttime,
                                'timestamp__lt': endtime,
                                'nolimit': True,
                            },
                            'plot_params': {
                                'linewidth': 1,
                                'label': 'Suhu termokopel 2',
                                'color': 'green'
                            },
                            'fields': ['timestamp', 'temperature2'],
                            'xaxis_date': True,
                            'axis': 1,
                            'formatter': {
                                'y': {
                                    'major': {
                                        'format': '%.1f'
                                    }
                                }
                            },
                            'locator': {
                                'y': {
                                    'major': {
                                        'name': 'MaxNLocator',
                                        'params': [7]
                                    }
                                }
                            },
                        },

                        {
                            'name': 'gas_emission',
                            'query_params': {
                                'timestamp__gte': starttime,
                                'timestamp__lt': endtime,
                                'nolimit': True,
                            },
                            'plot_params': {
                                'linewidth': 1,
                                'label': 'Suhu CO$_2$ maks.',
                                'color': 'purple'
                            },
                            'fields': ['timestamp', 'temperature_max'],
                            'xaxis_date': True,
                            'tertiary': {
                                'on': 'x',
                                'side': 'right',
                                'position': ('outward', 65)
                            },
                            'formatter': {
                                'y': {
                                    'major': {
                                        'format': '%.1f'
                                    }
                                }
                            },
                            'locator': {
                                'y': {
                                    'major': {
                                        'name': 'MaxNLocator',
                                        'params': [7]
                                    }
                                }
                            },
                            'labels': {
                                'y': {
                                    'text': r'Suhu CO$_2$ ($^\circ$C)'
                                }
                            },
                        },
                    ],
                    'legend': {
                        'show': True,
                        'loc': 'upper left',
                    }
                }
            ]
        },
        'extensions': {
            'starttime': starttime,
            'endtime': endtime,
            'plot': [
                {
                    'name': 'komapy.extensions.activity_status'
                },
                {
                    'name': 'komapy.extensions.explosion',
                    'label': 'Letusan',
                    'color': 'red'
                },
                {
                    'name': 'kompay.extensions.dome',
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

    }
    return config


chart = Chart(config_factory(starttime='2019-08-01', endtime='2019-11-16'))
chart.render()
chart.save('vogamos.png')
