# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 13:33:20 2020

@author: jakob
"""
# %% PACKAGES

# libs
import pickle
import time
from collections import OrderedDict

# own modules
from pysats import PySats

# %% Setup
model_name = "SRVM"
isLegacy = False
path = (
    "C://Users//jakob//PhD//Python_Projects//Sats//optimal_allocations//"
    + model_name
    + "//"
)
number_of_instances = 200
seeds_instances = list(range(1, 1 + number_of_instances))  # for instances in (1)
# %%
results = OrderedDict()

for instance in seeds_instances:
    print("INSTANCE", instance)
    if model_name == "GSVM":
        print(model_name + str(instance))
        auction_instance = PySats.getInstance().create_gsvm(
            seed=instance, isLegacyGSVM=isLegacy
        )  # (1)
    elif model_name == "LSVM":
        print(model_name + str(instance))
        auction_instance = PySats.getInstance().create_lsvm(
            seed=instance, isLegacyLSVM=isLegacy
        )  # (1)
    elif model_name == "MRVM":
        print(model_name + str(instance))
        auction_instance = PySats.getInstance().create_mrvm(seed=instance)  # (1)
    elif model_name == "SRVM":
        print(model_name + str(instance))
        auction_instance = PySats.getInstance().create_srvm(seed=instance)  # (1)
    else:
        raise NotImplementedError("No Value Model with name {}.".format(model_name))
    print("Solving WDP SATS:")
    start = time.time()
    allocation_SATS, value_SATS = auction_instance.get_efficient_allocation()
    end = time.time()
    del auction_instance
    print(
        "WDP SATS solved in " + time.strftime("%H:%M:%S", time.gmtime(end - start)),
        "\n",
    )
    print("Allocation:")
    for key in list(allocation_SATS.keys()):
        print(allocation_SATS[key])
    print("Value: ", value_SATS, "\n")
    results["Instance_Seed {}".format(instance)] = [allocation_SATS, value_SATS]

# SAVE results
if not isLegacy and model_name in ["LSVM", "GSVM"]:
    filename = "{}_isLegacy{}_optimal_allocations_seeds{}_{}.pkl".format(
        model_name, isLegacy, seeds_instances[0], seeds_instances[-1]
    )
else:
    filename = "{}_optimal_allocations_seeds{}_{}.pkl".format(
        model_name, seeds_instances[0], seeds_instances[-1]
    )

print("Saving as: ", filename)
f = open(path + filename, "wb")
pickle.dump(results, f)
f.close()
# %% Check
seeds_instances = list(range(1, 200 + 1))
f = open(
    path
    + "{}_optimal_allocations_seeds{}_{}.pkl".format(
        model_name, seeds_instances[0], seeds_instances[-1]
    ),
    "rb",
)
a = pickle.load(f)
f.close()

seed_instance = 33
auction_instance = PySats.getInstance().create_srvm(seed=seed_instance)
# auction_instance = PySats.getInstance().create_lsvm(seed=seed_instance, isLegacyGSVM=False)
# auction_instance = PySats.getInstance().create_mrvm(seed=seed_instance)

allocation_SATS, value_SATS = auction_instance.get_efficient_allocation()

print("SAVED allocation:")
for k, v in a["Instance_Seed {}".format(seed_instance)][0].items():
    print(k, v)
print()
print("CALCULATED allocation:")
for k, v in allocation_SATS.items():
    print(k, v)
print()
print("SAVED scw:")
print(a["Instance_Seed {}".format(seed_instance)][1])
print("CALCULATED scw:")
print(value_SATS)
print()
print("CHECK:")
print(
    "allocations equal:",
    a["Instance_Seed {}".format(seed_instance)][0] == allocation_SATS,
)
print("scws equal:", a["Instance_Seed {}".format(seed_instance)][1] == value_SATS)
