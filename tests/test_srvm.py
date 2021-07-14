import unittest
from pysats import PySats
import numpy as np

class SrvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_srvm(self):
        instance_seed=np.random.randint(1, 1000)
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print('\n\nMAIN TEST SRVM  | Seed:', instance_seed)
        bidder_ids = list(srvm.get_bidder_ids())
        print('Bidder IDs: {}'.format(bidder_ids))
        print('Good IDs: {}'.format(srvm.get_good_ids()))
        for bidder_id in bidder_ids:
            print('\nBidder {}'.format(bidder_id))
            bundle = np.random.binomial(1, 0.5, len(srvm.get_good_ids()))
            print(f'Query value for bundle {bundle}')
            value = srvm.calculate_value(bidder_id, bundle)
            print(f'value={value}')
            print('Generate 3 uniform random bids')
            bids = srvm.get_uniform_random_bids(bidder_id, 3)
            for bid in bids:
                print(bid)

        print('\nCalculate efficient allocation: goods | value')
        allocation, total_value = srvm.get_efficient_allocation()

        for k,v in allocation.items():
            tmp = f'Bidder_{k}: '
            goods = v['good_ids']
            value = v['value']
            tmp+=f'{goods} | {value}'
            print(tmp)
        print('\nCheck feasibility of (generic) efficient allocation')
        alloc_value = 0
        indicator_sum = np.zeros(len(srvm.get_good_ids()))
        for bidder, good_dict in allocation.items():
            print('\nBidder {}'.format(bidder))
            indicator = np.zeros(len(srvm.get_good_ids()),dtype=bool)
            indicator[np.asarray(good_dict['good_ids'], dtype=np.int32)] = 1
            print('Indicator alloc:', indicator.astype(np.float64))
            alloc_value += srvm.calculate_value(bidder, indicator)
            indicator_sum += indicator.astype(np.float64)
            print('Aggregated indicator alloc:', indicator_sum)
        self.assertAlmostEqual(alloc_value, total_value,places=4)
        self.assertTrue((indicator_sum <= 1).sum() == len(indicator_sum))

    def test_srvm_bid_seeds(self):
        instance_seed=2
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print('\n\nTEST SRVM random bid generators | Seed:', instance_seed)
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
        print('\n\nTEST SRVM multi instance generation | Seed:', instance_seed)
        bidder_ids = srvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print('Bidder: ', bidder_id)
        self.assertEqual(len(bidder_ids), 7)

    def test_goods_of_interest(self):
        instance_seed = 222
        srvm = self.pysats.create_srvm(seed=instance_seed)
        print('\n\nTEST SRVM goods of interest per bidder | Seed:', instance_seed)
        for bidder_id in srvm.get_bidder_ids():
            goods_of_interest = srvm.get_goods_of_interest(bidder_id)
            print(f'Bidder_{bidder_id}: {goods_of_interest}')


if __name__ == '__main__':
    unittest.main()
