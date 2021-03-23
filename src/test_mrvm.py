import unittest
from sats.pysats import PySats


class MrvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()


    def test_mrvm(self):
        instance_seed = 10
        mrvm = self.pysats.create_mrvm(seed=instance_seed)
        print('\n\n MAIN TEST MRVM  | Seed:', instance_seed)
        bidder_ids = list(mrvm.get_bidder_ids())
        print('Bidder IDs: {}'.format(bidder_ids))
        good_ids = list(mrvm.get_good_ids())
        print('Goods IDs: {}'.format(good_ids))
        for bidder_id in bidder_ids:
            print('\nBidder {}'.format(bidder_id))
            print('Query value for bundle')
            value = mrvm.calculate_value(
                bidder_id,
                [1, 0, 0, 1, 1, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0, 1, 0,
                 0, 1, 0, 0, 0, 1, 0, 0])
            print(f'value={value}')
            print('Generate 3 uniform random bids')
            bids = mrvm.get_uniform_random_bids(bidder_id, 3)
            for bid in bids:
                print(bid)

        print('\nCalculate efficient allocation: goods | value')
        allocation, total_value = mrvm.get_efficient_allocation()
        for k,v in allocation.items():
            tmp = f'Bidder_{k}: '
            goods = v['good_ids']
            value = v['value']
            tmp+=f'{goods} | {value}'
            print(tmp)
        self.assertEqual(allocation[bidder_ids[0]]['value'], 0)
        self.assertEqual(allocation[bidder_ids[1]]['value'], 0)
        self.assertEqual(allocation[bidder_ids[2]]['value'], 0)
        self.assertEqual(allocation[bidder_ids[3]]['value'], 0)
        self.assertEqual(round(allocation[bidder_ids[4]]['value'], 2),   132125599.55)
        self.assertEqual(round(allocation[bidder_ids[5]]['value'], 2),   122474729.64)
        self.assertEqual(round(allocation[bidder_ids[6]]['value'], 2),    12317777.67)
        self.assertEqual(round(allocation[bidder_ids[7]]['value'], 2),  1823597077.50)
        self.assertEqual(round(allocation[bidder_ids[8]]['value'], 2),  4760334228.38)
        self.assertEqual(round(allocation[bidder_ids[9]]['value'], 2),  2438399732.69)

    def test_mrvm_bid_seeds(self):
        instance_seed = 2
        mrvm = self.pysats.create_mrvm(seed=instance_seed)
        print('\n\n TEST MRVM random bid generators | Seed:', instance_seed)
        bidder_ids = mrvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = mrvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = mrvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)
            # Generate some bids with the new method
            bids = mrvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            new_bids = mrvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

    def test_multi_instance(self):
        instance_seed = 222
        mrvm = self.pysats.create_mrvm(seed=instance_seed)
        print('\n\n TEST MRVM multi instance generation | Seed:', instance_seed)
        bidder_ids = mrvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print('Bidder: ', bidder_id)
        self.assertEqual(len(bidder_ids), 10)

    def test_goods_of_interest(self):
        instance_seed = 111
        mrvm = self.pysats.create_mrvm()
        print('\n\n TEST MRVM goods of interest per bidder | Seed:', instance_seed)
        for bidder_id in mrvm.get_bidder_ids():
            goods_of_interest = mrvm.get_goods_of_interest(bidder_id)
            print(f'Bidder_{bidder_id}: {goods_of_interest}')

if __name__ == '__main__':
    unittest.main()
