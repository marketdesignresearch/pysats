# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:41:54 2020

@author: jakob
"""

from sats.pysats import PySats
import numpy as np
import pandas as pd

eff = {}
for i in range(1,101):
    print(i)
    gsvm = PySats.getInstance().create_gsvm(seed=i, isLegacyGSVM=True)

    bidder_ids = list(gsvm.get_bidder_ids())

    a = np.max([gsvm.calculate_value(bidder_id, [1]*18) for bidder_id in bidder_ids])

    allocation, total_value = gsvm.get_efficient_allocation()

    eff['Instance_{}'.format(i)] = a/total_value


EFF = pd.DataFrame.from_dict(eff, orient='index', columns=['EFF'])
print(EFF)
print(EFF.describe())