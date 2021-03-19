import unittest
from sats.pysats import PySats
import numpy as np

class GsvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_srvm(self):
        instance_seed=10
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print('Seed:', instance_seed)
        bidder_ids = list(srvm.get_bidder_ids())
        print('Bidder IDs: {}'.format(bidder_ids))
        print('Good IDs: {}'.format(srvm.get_good_ids()))
        for bidder_id in bidder_ids:
            # Query some value
            bundle = np.random.binomial(1, 0.5, len(srvm.get_good_ids()))
            value = srvm.calculate_value(
                bidder_id, bundle)
            print(value)
            # Generate some bids
            bids = srvm.get_random_bids(bidder_id, 10)
            print(bids)

        allocation, total_value = srvm.get_efficient_allocation()
        print(allocation)
        

    def test_srvm_bid_seeds(self):
        instance_seed=2
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print('Seed:', instance_seed)
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
        print('Seed:', instance_seed)
        bidder_ids = srvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print('Bidder: ', bidder_id)
        self.assertEqual(len(bidder_ids), 7)

    def test_goods_of_interest(self):
        instance_seed = 222
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print('Seed:', instance_seed)
        for bidder_id in srvm.get_bidder_ids():
            goods_of_interest = srvm.get_goods_of_interest(bidder_id)
            print(f'{srvm.population[bidder_id].getName()}: {goods_of_interest}')


if __name__ == '__main__':
    unittest.main()
