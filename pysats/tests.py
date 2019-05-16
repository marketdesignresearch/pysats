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

if __name__ == '__main__':
    unittest.main()
