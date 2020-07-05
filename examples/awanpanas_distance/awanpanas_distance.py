import os
import datetime
import locale
import pandas as pd

from komapy import Chart
from komapy.client import set_api_key
from komapy.transforms import register_transform
from komapy.series import register_addon

locale.setlocale(locale.LC_ALL, 'id_ID')

set_api_key(os.environ['API_KEY'])

starttime = '2019-01-01'
endtime = '2019-09-01'


@register_transform('compute_max_ap_distance')
def compute_max_ap_distance(data, config):
    df = pd.DataFrame()
    dfg = pd.DataFrame()

    df['eventdate'] = data[0]
    df['duration'] = data[1]

    dfg = df.groupby(df['eventdate'].dt.date).max()
    return [dfg['eventdate'].dt.date, dfg['duration']*10]


@register_addon('fix_zorder')
def fix_zorder(axis):
    axis.set_zorder(axis.get_zorder() + 100)
    axis.patch.set_visible(False)


@register_addon('draw_background')
def draw_background(axis):
    axis.grid(color='grey', linestyle='--', which='major', axis='y')

    date_when_level_increased = datetime.datetime(2018, 5, 21)
    axis.axvspan(starttime, date_when_level_increased,
                 alpha=0.4, color='lime', zorder=0)
    axis.axvspan(date_when_level_increased,
                 endtime, color='#fff59d', zorder=0)
    axis.set_xlim(starttime, endtime)

    axis.set_zorder(axis.get_zorder()-1)
    axis.patch.set_visible(False)


chart = Chart({
    'title': 'Jarak Luncur Awanpanas',
    'tight_layout': {
        'pad': 3,
        'w_pad': 1,
        'h_pad': 1
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
                            'label': 'Jumlah AP',
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
                                    'params': [7],
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
                                'text': 'Jumlah'
                            }
                        },
                        'addons': [
                            {
                                'name': 'fix_zorder'
                            }
                        ]
                    },
                    {
                        'type': 'line',
                        'name': 'bulletin',
                        'query_params': {
                            'eventtype': 'AWANPANAS',
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
                            'nolimit': True
                        },
                        'fields': ['eventdate', 'duration'],
                        'xaxis_date': True,
                        'plot_params': {
                            'label': 'Jarak Luncur AP',
                            'marker': 'o',
                            'markersize': 6,
                            'linewidth': 1,
                        },
                        'secondary': 'x',
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                        'transforms': [
                            'compute_max_ap_distance',
                        ],
                        'addons': [
                            {
                                'name': 'draw_background'
                            }
                        ],
                        'locator': {
                            'y': {
                                'major': {
                                    'name': 'MaxNLocator',
                                    'params': [8],
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
                                'text': 'Maksimum Jarak Luncur (m)'
                            }
                        }
                    },
                ],
                'legend': {
                    'show': True,
                    'loc': 'upper left',
                    'fancybox': False,
                    'framealpha': 0
                }
            }
        ]
    },
    'extensions': {
        'starttime': starttime,
        'endtime': endtime,
        'plot': [
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
chart.save('awanpanas_distance.png')
