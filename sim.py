import random

### 技能伤害 ###
def starFire_0(spellDamage, arcanePower):
    normalDamage = 666.6744 + 1.5246*(spellDamage+arcanePower)
    critDamage = normalDamage * 2.09
    return normalDamage, critDamage

def starFire_1(spellDamage, arcanePower):
    normalDamage = 842.1336 + 1.6632*(spellDamage+arcanePower)
    critDamage = normalDamage * 2.09
    return normalDamage, critDamage

def moonFire(spellDamage, arcanePower):
    normalDamage = 1290.366 + 0.92862*(spellDamage+arcanePower)
    critDamage = 1790.42 + 1.155*(spellDamage+arcanePower)
    dotDamage = 207.9 + 0.1805*(spellDamage+arcanePower)
    return normalDamage, critDamage, dotDamage
    
def insectSwarm(spellDamage):
    normalDamage = 831.6 + 0.84*spellDamage
    dotDamage = normalDamage/6
    return normalDamage, dotDamage

### 饰品模拟 ###
def icon(time, fadeTime): # trinket_1
    return 155*(time < fadeTime)

def quag(time, fadeTime): # trinket_2
    return 320/15.77*0.01*(time < fadeTime)

def Sextant(time, fadeTime): # trinket_3
    return 190*(time < fadeTime)

def Ashtongue(time, fadeTime): # trinket_4  
    return 150*(time < fadeTime)

### 伤害模拟 ###
# Icon and Quag, moonfire priority
def simulation1(totalTime, spellDamage, arcanePower, spellCrit, spellHit, spellHaste):
    faerieFireFade = 0.
    moonFireFade = 0.
    trinketFade_1 = 0.
    trinketFade_2 = 0.
    trinketCd_1 = 0.
    trinketCd_2 = 0.
    naturesGrace = 0
    time = 0.
    damage = 0.
    moonFireDot = 0.
    ffCast = 0
    mfCast = 0
    sfCast = 0
    
    while time < totalTime:
        if faerieFireFade - time < 3.:
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
        else:
            if (naturesGrace == 0 and moonFireFade - time < 3.) or (naturesGrace == 1 and moonFireFade - time < 2.5):
                mfCast += 1
                if moonFireFade > time:
                    damage -= moonFireDot
                moonFireDot = moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                    moonFireFade = time + 12
                time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                sfCast += 1
                if naturesGrace == 1:
                    time += max(3/(1 + spellHaste + quag(time, trinketFade_2)) - 0.5, 1.)
                    naturesGrace = 0
                else:
                    time += max(3/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            
    damage -= int(min(moonFireFade - totalTime, 0)/3)*moonFireDot
    return damage, ffCast, mfCast, sfCast

# Icon and Quag, starfire priority
def simulation2(totalTime, spellDamage, arcanePower, spellCrit, spellHit, spellHaste):
    faerieFireFade = 0.
    moonFireFade = 0.
    trinketFade_1 = 0.
    trinketFade_2 = 0.
    trinketCd_1 = 0.
    trinketCd_2 = 0.
    naturesGrace = 0
    time = 0.
    damage = 0.
    moonFireDot = 0.
    ffCast = 0
    mfCast = 0
    sfCast = 0
    
    while time < totalTime:
        if faerieFireFade - time < 3.:
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
        else:
            if moonFireFade - time < 0.:
                mfCast += 1
                moonFireDot = moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                    moonFireFade = time + 12
                time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                sfCast += 1
                if naturesGrace == 1:
                    time += max(3/(1 + spellHaste + quag(time, trinketFade_2)) - 0.5, 1.)
                    naturesGrace = 0
                else:
                    time += max(3/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        if moonFireFade - time < 0.:
                            damage += starFire_0(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        else:
                            damage += starFire_1(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        naturesGrace = 1
                    else:
                        if moonFireFade - time < 0.:
                            damage += starFire_0(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                        else:
                            damage += starFire_1(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            
    damage -= int(min(moonFireFade - totalTime, 0)/3)*moonFireDot
    return damage, ffCast, mfCast, sfCast

# Icon and Quag, starfire + insectswarm
def simulation3(totalTime, spellDamage, arcanePower, spellCrit, spellHit, spellHaste):
    faerieFireFade = 0.
    moonFireFade = 0.
    insectSwarmFade = 0.
    trinketFade_1 = 0.
    trinketFade_2 = 0.
    trinketCd_1 = 0.
    trinketCd_2 = 0.
    naturesGrace = 0
    time = 0.
    damage = 0.
    moonFireDot = 0.
    insectSwarmDot = 0.
    ffCast = 0
    mfCast = 0
    isCast = 0
    sfCast = 0
    
    while time < totalTime:
        if faerieFireFade - time < 3.:
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
        else:
            if moonFireFade < time and insectSwarmFade - time < 6.:
                mfCast += 1
                moonFireDot = moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                    moonFireFade = time + 12
                time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
            elif insectSwarmFade < time and moonFireFade - time < 6.:
                isCast += 1
                insectSwarmDot = insectSwarm(spellDamage + icon(time, trinketFade_1))[1]
                if random.random() < spellHit:
                    damage += insectSwarm(spellDamage + icon(time, trinketFade_1))[0]
                    insectSwarmFade = time + 12
                time += max(1.5/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                sfCast += 1
                if naturesGrace == 1:
                    time += max(3/(1 + spellHaste + quag(time, trinketFade_2)) - 0.5, 1.)
                    naturesGrace = 0
                else:
                    time += max(3/(1 + spellHaste + quag(time, trinketFade_2)), 1.)
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1), arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1), arcanePower)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            
    damage -= (int(min(moonFireFade - totalTime, 0)/3)*moonFireDot +\
               int(min(insectSwarmFade - totalTime, 0)/2)*insectSwarmDot)
    return damage, ffCast, mfCast, isCast, sfCast

# Icon and Sextant, moonfire priority
def simulation4(totalTime, spellDamage, arcanePower, spellCrit, spellHit, spellHaste):
    faerieFireFade = 0.
    moonFireFade = 0.
    trinketFade_1 = 0.
    trinketFade_3 = 0.
    trinketCd_1 = 0.
    trinketCd_3 = 0.
    naturesGrace = 0
    time = 0.
    damage = 0.
    moonFireDot = 0.
    ffCast = 0
    mfCast = 0
    sfCast = 0
    
    while time < totalTime:
        if faerieFireFade - time < 3.:
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(1.5/(1 + spellHaste), 1.)
        else:
            if (naturesGrace == 0 and moonFireFade - time < 3.) or (naturesGrace == 1 and moonFireFade - time < 2.5):
                mfCast += 1
                if moonFireFade > time:
                    damage -= moonFireDot
                moonFireDot = moonFire(spellDamage + icon(time, trinketFade_1) + Sextant(time, trinketFade_3),\
                                       arcanePower)[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1) + Sextant(time, trinketFade_3),\
                                           arcanePower)[1]
                        naturesGrace = 1
                        if trinketCd_3 <= time:
                            if random.random() < 0.2:
                                trinketCd_3 = time + 45
                                trinketFade_3 = time + 15
                    else:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1) + Sextant(time, trinketFade_3),\
                                           arcanePower)[0]
                    moonFireFade = time + 12
                time += max(1.5/(1 + spellHaste), 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                sfCast += 1
                if naturesGrace == 1:
                    time += max(3/(1 + spellHaste) - 0.5, 1.)
                    naturesGrace = 0
                else:
                    time += max(3/(1 + spellHaste), 1.)
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1) + Sextant(time, trinketFade_3),\
                                             arcanePower)[1]
                        naturesGrace = 1
                        if trinketCd_3 <= time:
                            if random.random() < 0.2:
                                trinketCd_3 = time + 45
                                trinketFade_3 = time + 15
                    else:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1) + Sextant(time, trinketFade_3),\
                                             arcanePower)[0]
                            
    damage -= int(min(moonFireFade - totalTime, 0)/3)*moonFireDot
    return damage, ffCast, mfCast, sfCast

# Icon and Ashtongue, moonfire priority
def simulation5(totalTime, spellDamage, arcanePower, spellCrit, spellHit, spellHaste):
    faerieFireFade = 0.
    moonFireFade = 0.
    trinketFade_1 = 0.
    trinketFade_4 = 0.
    trinketCd_1 = 0.
    naturesGrace = 0
    time = 0.
    damage = 0.
    moonFireDot = 0.
    ffCast = 0
    mfCast = 0
    sfCast = 0
    
    while time < totalTime:
        if faerieFireFade - time < 3.:
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(1.5/(1 + spellHaste), 1.)
        else:
            if (naturesGrace == 0 and moonFireFade - time < 3.) or (naturesGrace == 1 and moonFireFade - time < 2.5):
                mfCast += 1
                if moonFireFade > time:
                    damage -= moonFireDot
                moonFireDot = moonFire(spellDamage + icon(time, trinketFade_1) + Ashtongue(time, trinketFade_4),\
                                       arcanePower)[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1) + Ashtongue(time, trinketFade_4),\
                                           arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += moonFire(spellDamage + icon(time, trinketFade_1) + Ashtongue(time, trinketFade_4),\
                                           arcanePower)[0]
                    moonFireFade = time + 12
                time += max(1.5/(1 + spellHaste), 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                sfCast += 1
                if naturesGrace == 1:
                    time += max(3/(1 + spellHaste) - 0.5, 1.)
                    naturesGrace = 0
                else:
                    time += max(3/(1 + spellHaste), 1.)
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1) + Ashtongue(time, trinketFade_4),\
                                             arcanePower)[1]
                        naturesGrace = 1
                    else:
                        damage += starFire_1(spellDamage + icon(time, trinketFade_1) + Ashtongue(time, trinketFade_4),\
                                             arcanePower)[0]
                    if random.random() < 0.25:
                        trinketFade_4 = time + 8
                            
    damage -= int(min(moonFireFade - totalTime, 0)/3)*moonFireDot
    return damage, ffCast, mfCast, sfCast