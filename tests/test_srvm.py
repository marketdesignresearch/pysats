import unittest
from pysats import PySats
import numpy as np


class SrvmTest(unittest.TestCase):
    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_srvm(self):
        instance_seed = np.random.randint(1, 1000)
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print("\n\nMAIN TEST SRVM  | Seed:", instance_seed)
        bidder_ids = list(srvm.get_bidder_ids())
        print("Bidder IDs: {}".format(bidder_ids))
        print("Good IDs: {}".format(srvm.get_good_ids()))
        for bidder_id in bidder_ids:
            print("\nBidder {}".format(bidder_id))
            bundle = np.random.binomial(1, 0.5, len(srvm.get_good_ids()))
            print(f"Query value for bundle {bundle}")
            value = srvm.calculate_value(bidder_id, bundle)
            print(f"value={value}")
            print("Multiple bundles at once:")
            values = srvm.calculate_values(
                bidder_id,
                [
                    bundle,
                    np.random.binomial(1, 0.5, len(srvm.get_good_ids())),
                ],
            )
            print(f"values={values}")
            print("Generate 3 uniform random bids")
            bids = srvm.get_uniform_random_bids(bidder_id, 3)
            for bid in bids:
                print(bid)

        print("\nCalculate efficient allocation: goods | value")
        allocation, total_value = srvm.get_efficient_allocation()

        for k, v in allocation.items():
            tmp = f"Bidder_{k}: "
            goods = v["good_ids"]
            value = v["value"]
            tmp += f"{goods} | {value}"
            print(tmp)
        print("\nCheck feasibility of (generic) efficient allocation")
        alloc_value = 0
        indicator_sum = np.zeros(len(srvm.get_good_ids()))
        for bidder, good_dict in allocation.items():
            print("\nBidder {}".format(bidder))
            indicator = np.zeros(len(srvm.get_good_ids()), dtype=bool)
            indicator[np.asarray(good_dict["good_ids"], dtype=np.int32)] = 1
            print("Indicator alloc:", indicator.astype(np.float64))
            alloc_value += srvm.calculate_value(bidder, indicator)
            indicator_sum += indicator.astype(np.float64)
            print("Aggregated indicator alloc:", indicator_sum)
        self.assertAlmostEqual(alloc_value, total_value, places=4)
        self.assertTrue((indicator_sum <= 1).sum() == len(indicator_sum))

    def test_srvm_bid_seeds(self):
        instance_seed = 2
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print("\n\nTEST SRVM random bid generators | Seed:", instance_seed)
        bidder_ids = srvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = srvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = srvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)
            # Generate some bids with the new method
            bids = srvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            new_bids = srvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

    def test_multi_instance(self):
        instance_seed = 111
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print("\n\nTEST SRVM multi instance generation | Seed:", instance_seed)
        bidder_ids = srvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print("Bidder: ", bidder_id)
        self.assertEqual(len(bidder_ids), 7)

    def test_goods_of_interest(self):
        instance_seed = 222
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print("\n\nTEST SRVM goods of interest per bidder | Seed:", instance_seed)
        for bidder_id in srvm.get_bidder_ids():
            goods_of_interest = srvm.get_goods_of_interest(bidder_id)
            print(f"Bidder_{bidder_id}: {goods_of_interest}")

    def test_generic(self):

        print('---Starting SRVM test ---')

        srvm = PySats.getInstance().create_srvm(1)
        srvm_generic = PySats.getInstance().create_srvm(1, generic=True)

        self.assertEqual(len(srvm.get_good_ids()), 29)
        # Number of goods in GenericWrapper: 3
        self.assertEqual(len(srvm_generic.get_good_ids()), 3)

        # keys: goods, values: however many goods map to it
        capacities = {i: len(srvm_generic.good_to_licence[i]) for i in range(len(srvm_generic.good_to_licence))}
        capacities2 = srvm_generic.get_capacities()

        print('Generic capacities:', capacities)

        # compare the efficient allocation
        srvm_eff = srvm.get_efficient_allocation()
        srvm_generic_eff = srvm_generic.get_efficient_allocation()

        # efficient values are the same
        self.assertEqual(srvm_eff[1],srvm_generic_eff[1])

        # bidder allocation of original pysats (good refers to a licence)
        print(srvm_eff[0][1])
        # bidder allocation of generic wrapper (good refers to generic good), allocation contains additional good_count
        # (i.e. number of goods allocated in the same order as good_ids)
        print(srvm_generic_eff[0][1])

        # perform a demand query
        price = np.zeros(len(srvm_generic.get_good_ids()))
        demand = srvm_generic.get_best_bundles(1, price, 2, allow_negative=True)
        print(demand[0])
        print(len(demand[0]))

        # random queries work as expected
        bid = srvm_generic.get_uniform_random_bids(1, 1)[0]

        value = srvm_generic.calculate_value(1, demand[0])

        # ensuring that the value in 2 represetations is the same
        bundle_extended_representation = [0 for i in range(len(srvm.get_good_ids()))]
        for i in range(len(demand[0])):
            license_mapping = srvm_generic.good_to_licence[i]
            items_requested = demand[0][i]
            for j in range(items_requested):
                bundle_extended_representation[license_mapping[j]] = 1

        value_extended_representation = srvm.calculate_value(1, bundle_extended_representation)
        self.assertEqual(value, value_extended_representation)
        print('Difference between the values in the 2 representations:', value - value_extended_representation)


if __name__ == "__main__":
    unittest.main()
