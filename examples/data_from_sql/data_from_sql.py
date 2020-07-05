import os

from sqlalchemy import create_engine
from komapy import Chart

DATABASE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

engine = create_engine(DATABASE_URL)
sql = "select `timestamp`, `slope_distance` from `rb2` order by `timestamp` asc"

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
                    'sql': [sql, engine],
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
