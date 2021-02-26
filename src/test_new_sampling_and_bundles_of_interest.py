# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 12:57:55 2020

@author: jakob
"""

from sats.pysats import PySats
import numpy as np

# %%
instance_seed = 10
world = 'LSVM'
isLegacy = False

# %%

print('Value Model:', world)
if world == 'GSVM':
    auction = PySats.getInstance().create_gsvm(seed=instance_seed, isLegacyGSVM=isLegacy)
elif world == 'LSVM':
    auction = PySats.getInstance().create_lsvm(seed=instance_seed, isLegacyLSVM=isLegacy)
elif world == 'MRVM':
    auction = PySats.getInstance().create_mrvm(seed=instance_seed)
else:
    raise NotImplementedError('World not implemented')

for bidder_id in auction.get_bidder_ids():
    # new goods of interest
    goods_of_interest = auction.get_goods_of_interest(bidder_id)
    print(f'Items of Interest Bidder_{auction.population[bidder_id].getName()}:{goods_of_interest}\n')
    # new random sampling
    random_bid = np.asarray(auction.get_uniform_random_bids(bidder_id, 1, seed=11)) # setting a seed samples same bundle for all bidders!
    print(f'Random Uniform Bundle for Bidder_{auction.population[bidder_id].getName()} of Shape {random_bid.shape}:{random_bid}\n\nBundle Size: {np.sum(random_bid[:,:-1])}')
    print('\n')