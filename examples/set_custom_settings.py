from komapy.conf import settings

# Print default settings.
print(settings.as_dict())

# Set settings using attribute assignment.
settings.BMA_API_KEY = 'YOUR_API_KEY'
settings.DEFAULT_COLOR = '#272727'

# Set settings using dictionary object.
dict_settings = {
    'VELOCITY_RATE': 10,
    'NORMAL': {
        'alpha': 0.4,
        'color': 'lime',
        'zorder': 0,
    },
    'WASPADA': {
        'color': '#fff59d',
        'zorder': 0,
    },
}

settings.from_dict(dict_settings)

print(settings.as_dict())
