============================
Using External Configuration
============================

When we develop KomaPy in the first place, we design it to only use config to
create a customizable BPPTKG Monitoring API chart. Our design philosophy enable
users to create a chart config from a wide range of data types, including JSON,
XML, YAML, etc. It enable KomaPy to be easily embedded in the web framework for
particular usage.

Here it is an example of reading plot config from JSON data. Create a file and
append the following lines:

.. code-block:: json

    {
        "layout": {
            "data": [
                {
                    "series": [
                        {
                            "name": "edm",
                            "query_params": {
                                "start_at": "2019-04-01",
                                "end_at": "2019-08-01",
                                "benchmark": "BAB0",
                                "reflector": "RB2",
                                "ci": true
                            },
                            "fields": [
                                "timestamp",
                                "slope_distance"
                            ],
                            "xaxis_date": true
                        }
                    ]
                }
            ]
        }
    }

Save it to ``config.json``, then load the JSON file and pass the config data to
the chart class:

.. code-block:: python

    import json
    from komapy import Chart

    with open('config.json', 'r') as buf:
        config = json.load(buf)

    chart = Chart(config)
    chart.render()
    chart.save('figure.png')

For the data that comes from REST API, you can use ``json.loads`` instead of
``json.load`` because the data comes to you as JSON string.
