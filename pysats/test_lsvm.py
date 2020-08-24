import unittest
from pysats import PySats


class LsvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_lsvm(self):
        lsvm = self.pysats.create_lsvm(seed=2)
        bidder_ids = list(lsvm.get_bidder_ids())
        print('Bidder IDs: {}'.format(bidder_ids))
        print('Good IDs: {}'.format(lsvm.get_good_ids()))
        for bidder_id in bidder_ids:
            # Query some value
            value = lsvm.calculate_value(bidder_id, [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1])
            print(value)
            # Generate some bids
            bids = lsvm.get_random_bids(bidder_id, 10)
            print(bids)

        allocation, total_value = lsvm.get_efficient_allocation()
        print(allocation)
        self.assertEqual(allocation[bidder_ids[0]]['value'], 10.899624216435544)
        self.assertEqual(allocation[bidder_ids[1]]['value'], 14.863588882700238)
        self.assertEqual(allocation[bidder_ids[2]]['value'], 197.91229024726067)
        self.assertEqual(allocation[bidder_ids[3]]['value'], 0.0)
        self.assertEqual(allocation[bidder_ids[4]]['value'], 16.870979861919466)
        self.assertEqual(allocation[bidder_ids[5]]['value'], 209.7691468662042)

    def test_lsvm_bid_seeds(self):
        lsvm = self.pysats.create_lsvm(seed=2)
        bidder_ids = lsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = lsvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = lsvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)


if __name__ == '__main__':
    unittest.main()
