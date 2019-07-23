import unittest
from PySats import PySats


class MrvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()

    
    def test_mrvm(self):
        mrvm = self.pysats.create_mrvm(seed=10)
        bidder_ids = mrvm.get_bidder_ids()
        print('Bidder IDs: {}'.format(bidder_ids))
        for bidder_id in bidder_ids:
            # Query some value
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
            print(value)
            # Generate some bids
            bids = mrvm.get_random_bids(bidder_id, 10)
            print(bids)

        allocation, total_value = mrvm.get_efficient_allocation()
        print(allocation)
        self.assertEqual(allocation[0]['value'], 0)
        self.assertEqual(allocation[1]['value'], 0)
        self.assertEqual(allocation[2]['value'], 0)
        self.assertEqual(allocation[3]['value'], 0)
        self.assertEqual(round(allocation[4]['value'], 2),   132125599.55)
        self.assertEqual(round(allocation[5]['value'], 2),   122474729.64)
        self.assertEqual(round(allocation[6]['value'], 2),    12317777.67)
        self.assertEqual(round(allocation[7]['value'], 2),  1823597077.51)
        self.assertEqual(round(allocation[8]['value'], 2),  4760334228.43)
        self.assertEqual(round(allocation[9]['value'], 2),  2438399732.70)

    def test_mrvm_bid_seeds(self):
        mrvm = self.pysats.create_mrvm(seed=2)
        bidder_ids = mrvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = mrvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = mrvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

if __name__ == '__main__':
    unittest.main()
