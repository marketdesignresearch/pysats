import unittest
from PySats import PySats


class TestPySats(unittest.TestCase):
    
    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_lsvm(self):
        lsvm = self.pysats.create_lsvm(seed=2)
        bidder_ids = lsvm.get_bidder_ids()
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
        self.assertEqual(allocation[0]['value'], 10.899624216435544)
        self.assertEqual(allocation[1]['value'], 0)
        self.assertEqual(allocation[2]['value'], 197.9122902472607)
        self.assertEqual(allocation[3]['value'], 13.76196221807917)
        self.assertEqual(allocation[4]['value'], 20.5715648091427)
        self.assertEqual(allocation[5]['value'], 227.03173174626968)

    def test_lsvm_bid_seeds(self):
        lsvm = self.pysats.create_lsvm(seed=2)
        bidder_ids = lsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = lsvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = lsvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

    def test_gsvm(self):
        gsvm = self.pysats.create_gsvm(seed=10)
        bidder_ids = gsvm.get_bidder_ids()
        print('Bidder IDs: {}'.format(bidder_ids))
        print('Good IDs: {}'.format(gsvm.get_good_ids()))
        for bidder_id in bidder_ids:
            # Query some value
            value = gsvm.calculate_value(
                bidder_id, [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1])
            print(value)
            # Generate some bids
            bids = gsvm.get_random_bids(bidder_id, 10)
            print(bids)

        allocation, total_value = gsvm.get_efficient_allocation()
        print(allocation)
        self.assertEqual(allocation[0]['value'], 0)
        self.assertEqual(allocation[1]['value'], 337.8684035685592)
        self.assertEqual(allocation[2]['value'], 0)
        self.assertEqual(allocation[3]['value'], 199.12104698410005)
        self.assertEqual(allocation[4]['value'], 0)
        self.assertEqual(allocation[4]['value'], 0)

    def test_gsvm_bid_seeds(self):
        gsvm = self.pysats.create_gsvm(seed=2)
        bidder_ids = gsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = gsvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = gsvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

if __name__ == '__main__':
    unittest.main()
