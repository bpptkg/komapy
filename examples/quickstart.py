from komapy import Chart
from komapy.client import set_api_key

set_api_key('YOUR_API_KEY')

chart = Chart({
    'title': 'RB2',
    'theme': 'seaborn',
    'layout': {
        'data': [
            {
                'series': {
                    'name': 'edm',
                    'query_params': {
                        'benchmark': 'BAB0',
                        'reflector': 'RB2',
                        'start_at': '2019-04-01',
                        'end_at': '2019-08-01',
                        'ci': True
                    },
                    'fields': [
                        'timestamp',
                        'slope_distance'
                    ],
                    'xaxis_date': True
                }
            }
        ]
    }
})

chart.render()
chart.save('RB2.png')
