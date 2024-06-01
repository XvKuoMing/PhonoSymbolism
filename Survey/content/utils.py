import random

consonants = {
    'soft_palate': ['к', 'г'],
    'active_articulator': ['п', 'б', 'м'],
    'upper_teeth': ['т', 'д', 'н']
}

vowels = {
    'back': ['а', 'о', 'у'],
    'front': ['и', 'е']
}

cats = []
for _consonant in consonants.keys():
    for _vowel in vowels.keys():
        cats.append(
            (_consonant, _vowel)
            )

group = {**consonants,
         **vowels}


async def gen_brands_names(cv_n: int = 3):
    global group, cats
    brand_names = {}
    for consonant, vowel in cats:
        cons = group[consonant]
        vows = group[vowel]
        cvs = [
            random.choice(cons)+random.choice(vows) for _ in range(cv_n)
        ]
        cvs = ''.join(cvs)
        brand_names[cvs] = consonant+'+'+vowel
    return brand_names
