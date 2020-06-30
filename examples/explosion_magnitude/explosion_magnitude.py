import os
import locale

from komapy import Chart
from komapy.client import set_api_key

locale.setlocale(locale.LC_ALL, 'id_ID')

set_api_key(os.environ['API_KEY'])

chart = Chart({
    'title': 'Magnitudo Letusan 2018-2020',
    'tight_layout': {
        'pad': 3,
        'w_pad': 0.5,
        'h_pad': 0.5
    },
    'rc_params': {
        'font.size': 10,
        'font.sans-serif': ['Helvetica']
    },
    'layout': {
        'options': {
            'sharex': True,
            'figsize': [9, 5]
        },
        'data': [
            {
                'series': [
                    {
                        'name': 'magnitude',
                        'type': 'bar',
                        'query_params': {
                            'eventdate__gte': '2018-04-01',
                            'eventdate__lt': '2020-07-01',
                            'eventtype': 'EXPLOSION',
                            'nolimit': True,
                        },
                        'fields': ['eventdate', 'ml_pasarbubar'],
                        'xaxis_date': True,
                        'plot_params': {
                            'label': 'Magnitudo',
                            'color': 'k',
                        },
                        'labels': {
                            'y': {
                                'text': 'Magnitudo'
                            }
                        },
                        'formatter': {
                            'x': {
                                'major': {
                                    'name': 'DateFormatter',
                                    'params': ['%b %Y']
                                }
                            }
                        },
                    }
                ]
            }
        ]
    },
    'extensions': {
        'starttime': '2018-04-01',
        'endtime': '2020-07-01',
        'plot': [
            {
                'name': 'komapy.extensions.activity_status'
            }
        ]
    }
})

chart.render()
chart.save('magnitude.png')
