# Investment Opportunities
SEMEN_CANDLE = "Semen Candle"
SUN_SUITS = "Sun Suits"

# Risk Levels
LOW_RISK = "Low-Risk"
MEDIUM_RISK = "Medium-Risk"
HIGH_RISK = "High-Risk"
MAX_RISK = "Max-Risk"

Investment_Opportunities = [
    {'name': SEMEN_CANDLE,
     'description': 'A normal candle with the essence of man.',
     'risk_level': MEDIUM_RISK,
     'success_text': "Semen Candle has become the #1 selling candle in the Shebokken.",
     'failure_text': "Semen Candle has gone under following a unanimous lack of interest."
     },
    {'name': SUN_SUITS,
     'description': 'Wearable. Washable. Sun Suits.',
     'risk_level': MEDIUM_RISK,
     'success_text': "Sun Suits have taken over as the preferred method of UV protection.",
     'failure_text': "Sun Suits have been discontinued after chemical leeching has lured\n"
                     "hundreds of great white sharks to the beaches of Shebokken."
     },
]

Risk_Levels = [
    {
        'name': LOW_RISK,
        'min_levels': 1,
        'max_levels': 2,
        'success_rate': 0.80,
        'min_multiplier': 1.5,
        'max_multiplier': 2.0,
    },
    {
        'name': MEDIUM_RISK,
        'min_levels': 2,
        'max_levels': 3,
        'success_rate': 0.50,
        'min_multiplier': 2.0,
        'max_multiplier': 4.0,
    },
    {
        'name': HIGH_RISK,
        'min_levels': 3,
        'max_levels': 4,
        'success_rate': 0.25,
        'min_multiplier': 4.0,
        'max_multiplier': 8.0,
    },
    {
        'name': MAX_RISK,
        'min_levels': 5,
        'max_levels': 6,
        'success_rate': 0.10,
        'min_multiplier': 5.0,
        'max_multiplier': 10.0,
    },
]
