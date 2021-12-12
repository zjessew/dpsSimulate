import random
import numpy as np
import sim

### 面板属性 ###

intellect_0 = 424
spellDamage_0 = 1084
arcanePower_0 = 50
spellCrit_0 = 0.1974
spellHit_0 = 0.1201
spellHaste_0 = 0.
'''
intellect_0 = 424
spellDamage_0 = 1047
arcanePower_0 = 50
spellCrit_0 = 0.2156
spellHit_0 = 0.1201
spellHaste_0 = 0.
'''
### 团队属性 ###
intellect = (intellect_0 + 40 + 18)*1.1
spellDamage = spellDamage_0 + (intellect-intellect_0)*0.25 + 23 + 36 + 101 + 24
arcanePower = arcanePower_0 + 80
spellCrit = spellCrit_0 + (intellect-intellect_0)/79.4*0.01 + 0.05 + 0.0063 + 0.03 + 0.03
spellHit = min(0.83 + spellHit_0 + 0.04, 0.99)
spellHaste = spellHaste_0

### 调用模拟函数 ###
def simulation(simFuntion, totalTime, spellDamage = spellDamage, arcanePower = arcanePower,\
               spellCrit = spellCrit, spellHit = spellHit, spellHaste = spellHaste):
    return simFuntion(totalTime, spellDamage = spellDamage, arcanePower = arcanePower,\
               spellCrit = spellCrit, spellHit = spellHit, spellHaste = spellHaste)

total1 = np.zeros(3)
for i in range(1000):
    total1[0] += simulation(sim.simulation1, 200)[0]
    total1[1] += simulation(sim.simulation2, 200)[0]
    total1[2] += simulation(sim.simulation3, 200)[0]
dps1 = total1/1000/200

total2 = np.zeros(3)
for i in range(1000):
    total2[0] += simulation(sim.simulation1, 300)[0]
    total2[1] += simulation(sim.simulation2, 300)[0]
    total2[2] += simulation(sim.simulation3, 300)[0]
dps2 = total2/1000/300

total3 = np.zeros(3)
for i in range(1000):
    total3[0] += simulation(sim.simulation1, 500)[0]
    total3[1] += simulation(sim.simulation2, 500)[0]
    total3[2] += simulation(sim.simulation3, 500)[0]
dps3 = total3/1000/500
