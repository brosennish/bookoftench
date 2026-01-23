import random

from savethewench.data.enemies import *

Enemy_Lines = {
    BANDIT: ["Give me all of your coin, or else!",
             "I stole coin from an old lady today... or was that yesterday?",
             "I live to steal and steal to live... or, maybe I just steal to steal?"],
    GOON: ["I'll do anything for coin, as long as it's violent.",
           "Without my sunglasses, I'm nothing...",
           "I often call Sir. Michelob Chounce Esquire for legal support on account of my violent lifestyle."],
    PIMP: ["I love my hoes.",
           "If you die, I promise to give my hoes a better life.",
           "Hoes or not, I sure do love them."],
    HOBO: ["Give me those coins or I'll chop off your loins!",
           "I ate a rapper yesterday. No 'w'.",
           "People never give me coin unless I kill them.",
           "You know how much candy I can buy with just a small amount of coin!"],
    SERIAL_KILLER: ["If God taketh away, but I take your life... am I not, then, God?",
                    "God can do a lot, but he can't do the things I can do to you.",
                    "Glory be to he who kills... the glory hole's at Bayou Bill's."],
    HIKER: ["I'm in the woods, so you must be a murderer. I've seen movies!",
            "Are chipmunks dangerous? I figure if there's enough of them they could take me out...",
            "All mushrooms are safe to eat, right?"],
    DISGRACED_EXILE: ["You know, life was actually worse before I became a disgrace and was exiled.",
                      "If the town understood why I tried to burn it down, maybe they wouldn't have exiled me.",
                      "They didn't exile me I exiled them... from myself."],
    HUNTER: ["I kill things when I don't have to... and I enjoy it!",
             "Why hang out with girls when I can be out here in the freezing cold hunting by myself?",
             "Once I got bored of hunting animals, I started hunting people instead. You know, just for fun."],
    POACHER: ["Protected species? More like I'm going to put its head on my wall, species.",
              "Tusks are sharp, but I'm the sharpest.",
              "People pay me coin to kill illegal stuff. So what? Sue me! Well, don't do that, actually."],
    MINER: ["I thought I found some coal a month ago... turns out bat shit looks a lot like coal in the pitch dark.",
            "I nearly had a heart attack when I heard a man talking in the mine. Turns out it was just me, talking to myself.",
            "All of my friends worked in these mines. They're all dead now. Maybe I should get a different job?"],
    SPELUNKER: ["I haven't found anything, but my mom always says I'm the real treasure."
                "I got into this because of a video game... and now I'm in one! I hate irony... but I love iron!",
                "People think spelunking is just playing around in dark, wet holes."],
    MOLE_PERSON: ["fircnosdnvkclgnsdksnlfdkdfmkmc",
                  "orihgeoiwsifdjnwsietnvirodbrgnioevndoirng",
                  "ihfedkjnefdnefidnifnidn"],
    HUMANOID_CAVE_CREATURE: ["God may be merciful... loving... but I am not God. I am not God.",
                             "You think you're holy... but you are not holy. Do you live in a hole? Like me?",
                             "I am one with God, because I am God. You are merely an ant."],
    HAND_FISHERMAN: ["If you count your hand as a catch, you catch something every time! Unless a catfish bites it off...",
                     "I'd use a pole but the fish are just way too big. They ate my first three born.",
                     "One time I pulled a man out of a hole. I put him back because I wasn't fishing for men that day."],
    VOODOO_PRIESTESS: ["I will shrink your head, then raise the dead, then shrink their heads, 'cause I love shrinkin' heads.",
                       "I can tell you your future... It's very dark. Soon, you will see what I mean.",
                       "Does it drive you crazy then I shake my stick?"],
    BAYOU_MAN: ["When you livin' out here in the bayou ain't nobody come 'round.",
                "Without some fresh feed it's easy for a boy to come up cold out here on the bayou.",
                "Riverboat, Crawdad, Alligator Gumbo!"],
    SKIN_COLLECTOR: ["I don't just collect skins... I collect souls too.",
                     "Your skin looks very comfortable. May I try it on?",
                     "Where did you get your skin? It's so... fresh."],
    }


def get_enemy_encounter_line(enemy) -> str | None:
    if enemy.name not in Enemy_Lines:
        return None
    return random.choice(Enemy_Lines[enemy.name])
