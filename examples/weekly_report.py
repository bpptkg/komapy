import pytz
import datetime

from komapy import Chart
from komapy.client import set_api_key
from komapy.extensions import register_extension
from komapy.constants import TIME_ZONE

set_api_key('YOUR_API_KEY')

DAYS_TIMESPAN = 180
DATE_FORMAT = r'%Y-%m-%d'

end = datetime.datetime.now(pytz.timezone(TIME_ZONE))
start = end - datetime.timedelta(days=DAYS_TIMESPAN)

starttime = start.strftime(DATE_FORMAT)
endtime = end.strftime(DATE_FORMAT)


def plot_activity_status(axis, starttime, endtime):
    """
    Plot activity status color.
    """

    handle = None
    date_when_level_increased = datetime.datetime(2018, 5, 21)
    axis.axvspan(starttime, date_when_level_increased,
                 alpha=0.4, color='lime', zorder=0)
    axis.axvspan(date_when_level_increased,
                 endtime, color='#fff59d', zorder=0)
    axis.set_xlim(starttime, endtime)

    return handle


register_extension('activity_status', plot_activity_status)


chart = Chart({
    'tight_layout': {
        'pad': 3,
        'w_pad': 0.5,
        'h_pad': 0.6
    },
    'layout': {
        'options': {
            'sharex': True,
            'figsize': [12, 14]
        },
        'data': [
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'VTA',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'VTA'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'VTA'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'VTB',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'VTB'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'VTB'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'MP',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'MP'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'MP'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'LF',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'LF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'LF'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'ROCKFALL',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'RF'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'RF'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'GASBURST',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'DG'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'DG'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'seismicity',
                        'type': 'bar',
                        'query_params': {
                            'eventtype': 'AWANPANAS',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'label': 'AP'
                        },
                        'fields': ['timestamp', 'count'],
                        'xaxis_date': True,
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5],
                                    'keyword_params': {
                                        'integer': True
                                    }
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'AP'
                            }
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'edm',
                        'query_params': {
                            'start_at': starttime,
                            'end_at': endtime,
                            'benchmark': 'KAL0',
                            'reflector': 'RK2',
                            'ci': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'marker': 'o',
                            'markersize': 6,
                            'zorder': 2,
                            'linewidth': 1,
                            'label': 'RK2'
                        },
                        'fields': ['timestamp', 'slope_distance'],
                        'xaxis_date': True,
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
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5]
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'meter'
                            }
                        },
                        'legend': {
                            'show': True,
                            'loc': 'upper left'
                        }
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'edm',
                        'query_params': {
                            'start_at': starttime,
                            'end_at': endtime,
                            'benchmark': 'BAB0',
                            'reflector': 'RB2',
                            'ci': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'marker': 'o',
                            'markersize': 6,
                            'zorder': 2,
                            'linewidth': 1,
                            'label': 'RB2'
                        },
                        'fields': ['timestamp', 'slope_distance'],
                        'xaxis_date': True,
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
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5]
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'meter'
                            }
                        },
                        'legend': {
                            'show': True,
                            'loc': 'upper left'
                        },
                    }
                ]
            },
            {
                'series': [
                    {
                        'name': 'gps_baseline',
                        'query_params': {
                            'timestamp__gte': starttime,
                            'timestamp__lt': endtime,
                            'station1': 'pasarbubar',
                            'station2': 'selo',
                            'nolimit': True
                        },
                        'plot_params': {
                            'color': 'k',
                            'marker': 'o',
                            'markersize': 6,
                            'zorder': 2,
                            'linewidth': 1,
                            'label': 'PASB-SELO',
                        },
                        'fields': ['timestamp', 'baseline'],
                        'xaxis_date': True,
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
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [5]
                                }
                            },
                            'x': {
                                'major': {
                                    'name': 'MonthLocator'
                                }
                            }
                        },
                        'labels': {
                            'y': {
                                'text': 'meter'
                            }
                        },
                        'legend': {
                            'show': True,
                            'loc': 'upper left'
                        }
                    }
                ]
            },
        ]
    },
    'extensions': {
        'starttime': starttime,
        'endtime': endtime,
        'plot': [
            {
                'name': 'activity_status'
            },
            {
                'name': 'explosion',
                'label': 'Letusan',
                'color': 'red'
            },
            {
                'name': 'dome',
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
chart.save(
    'weekly_report_{}.png'.format(
        datetime.datetime.now(
            pytz.timezone(TIME_ZONE)
        ).strftime('%Y-%m-%d_%H-%M-%S')
    ))
