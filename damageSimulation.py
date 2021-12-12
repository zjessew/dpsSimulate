import random
import numpy as np

### 面板属性 ###
intellect_0 = 424
spellDamage_0 = 1084
arcanePower_0 = 50
spellCrit_0 = 0.1974
spellHit_0 = 0.1201
spellHaste_0 = 0.

### 团队属性 ###
intellect = (intellect_0 + 40 + 18)*1.1
spellDamage = spellDamage_0 + (intellect-intellect_0)*0.25 + 23 + 36 + 101 + 24
arcanePower = arcanePower_0 + 80
spellCrit = spellCrit_0 + (intellect-intellect_0)/79.4*0.01 + 0.05 + 0.0063 + 0.03 + 0.03
spellHit = min(0.83 + spellHit_0 + 0.04, 0.99)
spellHaste = spellHaste_0

### 技能伤害 ###
def starFire_0(spellDamage, arcanePower, spellHaste):
    normalDamage = 666.6744 + 1.5246*(spellDamage+arcanePower)
    critDamage = normalDamage * 2.09
    cast = 3/(1+spellHaste)
    return normalDamage, critDamage, cast

def starFire_1(spellDamage, arcanePower, spellHaste):
    normalDamage = 842.1336 + 1.6632*(spellDamage+arcanePower)
    critDamage = normalDamage * 2.09
    cast = 3/(1+spellHaste)
    return normalDamage, critDamage, cast

def moonFire(spellDamage, arcanePower, spellHaste):
    normalDamage = 1290.366 + 0.92862*(spellDamage+arcanePower)
    critDamage = 1790.42 + 1.155*(spellDamage+arcanePower)
    dotDamage = 207.9 + 0.1805*(spellDamage+arcanePower)
    cast = 1.5/(1+spellHaste)
    return normalDamage, critDamage, dotDamage, cast
    
def insectSwarm(spellDamage, spellHaste):
    normalDamage = 831.6 + 0.84*spellDamage
    dotDamage = normalDamage/6
    cast = 1.5/(1+spellHaste)
    return normalDamage, dotDamage, cast

def faerieFire(spellHaste):
    return 1.5/(1+spellHaste)

### 伤害模拟 ###
def simlation1(totalTime, intellect = intellect, spellDamage = spellDamage, arcanePower = arcanePower,\
               spellCrit = spellCrit, spellHit = spellHit, spellHaste = spellHaste):
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
    spellDamage_1 = spellDamage
    spellHaste_1 = spellHaste
    
    while time < totalTime:
        if time > trinketFade_2:
            spellHaste_1 = spellHaste
        if faerieFireFade - time < 3.:
            faerieFireInf = faerieFire(spellHaste_1)
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(faerieFireInf, 1.)
        else:
            if (naturesGrace == 0 and moonFireFade - time < 3.) or (naturesGrace == 1 and moonFireFade - time < 2.5):
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                moonFireInf = moonFire(spellDamage_1, arcanePower, spellHaste_1)
                mfCast += 1
                if moonFireFade > time:
                    damage -= moonFireDot
                moonFireDot = moonFireInf[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFireInf[1]
                        naturesGrace = 1
                    else:
                        damage += moonFireInf[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            spellHaste_1 = spellHaste + 320/15.77*0.01
                    moonFireFade = time + 12
                time += max(moonFireInf[3], 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                    spellDamage_1 = spellDamage + 155
                starFireInf = starFire_1(spellDamage_1, arcanePower, spellHaste_1)
                sfCast += 1
                if naturesGrace == 1:
                    time += starFireInf[2] - 0.5
                    naturesGrace = 0
                else:
                    time += starFireInf[2]
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        damage += starFire_1(spellDamage_1, arcanePower, spellHaste_1)[1]
                        naturesGrace = 1
                    else:
                        damage += starFire_1(spellDamage_1, arcanePower, spellHaste_1)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            spellHaste_1 = spellHaste + 320/15.77*0.01
                            
    damage -= int(min(moonFireFade - totalTime, 0)/3)*moonFireDot
    return damage, ffCast, mfCast, sfCast

def simlation2(totalTime, intellect = intellect, spellDamage = spellDamage, arcanePower = arcanePower,\
               spellCrit = spellCrit, spellHit = spellHit, spellHaste = spellHaste):
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
    spellDamage_1 = spellDamage
    spellHaste_1 = spellHaste
    
    while time < totalTime:
        if time > trinketFade_2:
            spellHaste_1 = spellHaste
        if faerieFireFade - time < 3.:
            faerieFireInf = faerieFire(spellHaste_1)
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(faerieFireInf, 1.)
        else:
            if moonFireFade < time:
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                moonFireInf = moonFire(spellDamage_1, arcanePower, spellHaste_1)
                mfCast += 1
                moonFireDot = moonFireInf[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFireInf[1]
                        naturesGrace = 1
                    else:
                        damage += moonFireInf[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            spellHaste_1 = spellHaste + 320/15.76*0.01
                    moonFireFade = time + 12
                time += max(moonFireInf[3], 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                    spellDamage_1 = spellDamage + 155
                starFireInf = starFire_1(spellDamage_1, arcanePower, spellHaste_1)
                sfCast += 1
                if naturesGrace == 1:
                    time += starFireInf[2] - 0.5
                    naturesGrace = 0
                else:
                    time += starFireInf[2]
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        if moonFireFade < time:
                            damage += starFire_0(spellDamage_1, arcanePower, spellHaste_1)[1]
                        else:
                            damage += starFire_1(spellDamage_1, arcanePower, spellHaste_1)[1]
                        naturesGrace = 1
                    else:
                        if moonFireFade < time:
                            damage += starFire_0(spellDamage_1, arcanePower, spellHaste_1)[0]
                        else:
                            damage += starFire_1(spellDamage_1, arcanePower, spellHaste_1)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            spellHaste_1 = spellHaste + 320/15.76*0.01
                            
    damage -= int(min(moonFireFade - totalTime, 0)/3)*moonFireDot
    return damage, ffCast, mfCast, sfCast

def simlation3(totalTime, intellect = intellect, spellDamage = spellDamage, arcanePower = arcanePower,\
               spellCrit = spellCrit, spellHit = spellHit, spellHaste = spellHaste):
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
    spellDamage_1 = spellDamage
    spellHaste_1 = spellHaste
    
    while time < totalTime:
        if time > trinketFade_2:
            spellHaste_1 = spellHaste
        if faerieFireFade - time < 3.:
            faerieFireInf = faerieFire(spellHaste_1)
            ffCast += 1
            if random.random() < spellHit:
                faerieFireFade = time + 40
            time += max(faerieFireInf, 1.)
        else:
            if moonFireFade < time and insectSwarmFade - time < 6:
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                moonFireInf = moonFire(spellDamage_1, arcanePower, spellHaste_1)
                mfCast += 1
                moonFireDot = moonFireInf[2]
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.1:
                        damage += moonFireInf[1]
                        naturesGrace = 1
                    else:
                        damage += moonFireInf[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            spellHaste_1 = spellHaste + 320/15.77*0.01
                    moonFireFade = time + 12
                time += max(moonFireInf[3], 1.)
            elif insectSwarmFade < time and moonFireFade - time < 6:
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                insectSwarmInf = insectSwarm(spellDamage_1, spellHaste_1)
                isCast += 1
                insectSwarmDot = insectSwarmInf[1]
                if random.random() < spellHit:
                    damage += insectSwarmInf[0]
                    insectSwarmFade = time + 12
                time += max(insectSwarmInf[2], 1.)
            else:
                if trinketCd_1 <= time:
                    trinketCd_1 = time + 120
                    trinketFade_1 = time + 20
                    spellDamage_1 = spellDamage + 155
                starFireInf = starFire_1(spellDamage_1, arcanePower, spellHaste_1)
                sfCast += 1
                if naturesGrace == 1:
                    time += starFireInf[2] - 0.5
                    naturesGrace = 0
                else:
                    time += starFireInf[2]
                if time > trinketFade_1:
                    spellDamage_1 = spellDamage
                if random.random() < spellHit:
                    if random.random() < spellCrit + 0.04:
                        damage += starFire_1(spellDamage_1, arcanePower, spellHaste_1)[1]
                        naturesGrace = 1
                    else:
                        damage += starFire_1(spellDamage_1, arcanePower, spellHaste_1)[0]
                    if trinketCd_2 <= time:
                        if random.random() < 0.1:
                            trinketCd_2 = time + 45
                            trinketFade_2 = time + 6
                            spellHaste_1 = spellHaste + 320/15.77*0.01
                            
    damage -= (int(min(moonFireFade - totalTime, 0)/4)*moonFireDot + \
               int(min(insectSwarmFade - totalTime, 0)/6)*moonFireDot)
    return damage, ffCast, mfCast, isCast, sfCast

total = np.zeros(3)
for i in range(100):
    total[0] += simlation1(200)[0]
    total[1] += simlation2(200)[0]
    total[2] += simlation3(200)[0]
    