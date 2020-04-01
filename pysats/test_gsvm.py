import unittest
from PySats import PySats


class GsvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()
    
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

        allocation, total_value = gsvm.get_efficient_allocation(
            allowAssigningLicensesWithZeroBasevalue=False)
        print(allocation)
        self.assertEqual(allocation[0]['value'], 0)
        self.assertEqual(allocation[1]['value'], 211.1677522303495)
        self.assertEqual(allocation[2]['value'], 0)
        self.assertEqual(allocation[3]['value'], 199.12104698410005)
        self.assertEqual(allocation[4]['value'], 0)
        self.assertEqual(allocation[5]['value'], 145.4180879903979)
        self.assertEqual(allocation[6]['value'], 0)

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
