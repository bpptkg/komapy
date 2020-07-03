import os
import locale

from komapy import Chart
from komapy.client import set_api_key
from komapy.transforms import register_transform

locale.setlocale(locale.LC_ALL, 'id_ID')

set_api_key(os.environ['API_KEY'])

startime = '2018-04-01'
endtime = '2020-07-01'


@register_transform('compute_seismic_energy')
def compute_seismic_energy(data, config):
    """
    Compute seismic energy from magnitude. Return energy in MJ unit.
    """
    energy = 10**(11.8 + 1.5 * data[1]) / 10**12
    return [data[0], energy / 10]


chart = Chart({
    'title': 'Energi Seismik Letusan 2018-2020',
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
                            'eventdate__gte': startime,
                            'eventdate__lt': endtime,
                            'eventtype': 'EXPLOSION',
                            'nolimit': True,
                        },
                        'fields': ['eventdate', 'ml_pasarbubar'],
                        'xaxis_date': True,
                        'transforms': [
                            'compute_seismic_energy',
                        ],
                        'plot_params': {
                            'label': 'Energi',
                            'color': 'k',
                        },
                        'labels': {
                            'y': {
                                'text': 'Energi Seismik (MJ)'
                            }
                        },
                    }
                ]
            }
        ]
    },
    'extensions': {
        'starttime': startime,
        'endtime': endtime,
        'plot': [
            {
                'name': 'komapy.extensions.activity_status'
            }
        ]
    }
})

chart.render()
chart.save('energy.png')
