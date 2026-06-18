# Investment Opportunities
BOBS_BOXES = "Bob Robertson's Door-to-Door Cardboard Box Delivery Business"
MAIL_ORDER_EGGS = "Mail Order Eggs"
SEMEN_CANDLE = "Semen Candle"
SUN_SUITS = "Sun Suits"

# Risk Levels
LOW_RISK = "Low"
MEDIUM_RISK = "Medium"
HIGH_RISK = "High"
MAX_RISK = "Max"

Investment_Opportunities = [
    {'name': BOBS_BOXES,
     'description': 'Just some awkward guy who attempts to deliver cardboard boxes door-to-door.',
     'risk_level': HIGH_RISK,
     'success_text': "Bob Robertson has become the official cardboard box deliverer for the City of Shebokken!",
     'failure_text': "Bob Robertson was brutally murdered by a small, angry woman for trespassing."
     },
    {'name': MAIL_ORDER_EGGS,
     'description': 'Eggs - Vacuum sealed, straight to your mailbox.',
     'risk_level': MEDIUM_RISK,
     'success_text': "Mail Order Eggs have taken over Shebokken! Citizens are refusing to eat anything else.",
     'failure_text': "Thousands have died from eating rotten eggs delivered via the post.\nMail Order Eggs is being sued for billions."
     },
    {'name': SEMEN_CANDLE,
     'description': 'A suspicious candle with a masculine, seedy aroma.',
     'risk_level': HIGH_RISK,
     'success_text': "Semen Candle has become the #1 selling candle in the Shebokken!",
     'failure_text': "Semen Candle has gone under following a unanimous lack of interest."
     },
    {'name': SUN_SUITS,
     'description': 'Wearable. Washable. Fully transparent. Sun Suits.',
     'risk_level': MEDIUM_RISK,
     'success_text': "Sun Suits have taken over as the preferred method of UV protection!",
     'failure_text': "Sun Suits have been discontinued after chemical leeching has lured\n"
                     "hundreds of great white sharks to the beaches of Shebokken."
     },
]

Risk_Levels = [
    {
        'name': LOW_RISK,
        'min_levels': 1,
        'max_levels': 2,
        'min_success_rate': 0.75,
        'max_success_rate': 0.85,
        'min_multiplier': 1.5,
        'max_multiplier': 2.0,
    },
    {
        'name': MEDIUM_RISK,
        'min_levels': 2,
        'max_levels': 3,
        'min_success_rate': 0.40,
        'max_success_rate': 0.60,
        'min_multiplier': 2.0,
        'max_multiplier': 4.0,
    },
    {
        'name': HIGH_RISK,
        'min_levels': 3,
        'max_levels': 4,
        'min_success_rate': 0.15,
        'max_success_rate': 0.35,
        'min_multiplier': 4.0,
        'max_multiplier': 8.0,
    },
    {
        'name': MAX_RISK,
        'min_levels': 5,
        'max_levels': 6,
        'min_success_rate': 0.08,
        'max_success_rate': 0.12,
        'min_multiplier': 6.0,
        'max_multiplier': 12.0,
    },
]
