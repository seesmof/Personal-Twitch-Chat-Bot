import random

emotes_greet = ["PotFriend", "KonCha", "SUBprise", "TPFufun", "TehePelo", "BegWan", "Poooound",
                "GivePLZ", "DxCat", "bleedPurple", "RitzMitz", "<3", "VoHiYo", "RaccAttack", "GlitchCat", "HeyGuys"]
emotes_hand = ["✋", "✌️", "👐", "👋", "🤚", "🤙"]

for i in range(20):
    print(random.choice(emotes_greet + emotes_hand))
