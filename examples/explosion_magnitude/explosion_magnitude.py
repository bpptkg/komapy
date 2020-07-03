import os
import locale

from komapy import Chart
from komapy.client import set_api_key

locale.setlocale(locale.LC_ALL, 'id_ID')

set_api_key(os.environ['API_KEY'])

starttime = '2018-04-01'
endtime = '2020-07-01'


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
                            'eventdate__gte': starttime,
                            'eventdate__lt': endtime,
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
                    }
                ]
            }
        ]
    },
    'extensions': {
        'starttime': starttime,
        'endtime': endtime,
        'plot': [
            {
                'name': 'komapy.extensions.activity_status'
            }
        ]
    }
})

chart.render()
chart.save('magnitude.png')
