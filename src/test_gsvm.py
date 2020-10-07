import unittest
from sats.pysats import PySats


class GsvmTest(unittest.TestCase):

    def setUp(self):
        self.pysats = PySats.getInstance()

    def test_gsvm(self):
        instance_seed=10
        gsvm = self.pysats.create_gsvm(seed=instance_seed, isLegacyGSVM=False)
        print('Seed:', instance_seed)
        bidder_ids = list(gsvm.get_bidder_ids())
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
        self.assertEqual(allocation[bidder_ids[0]]['value'], 63.956524457507044)
        self.assertEqual(allocation[bidder_ids[1]]['value'], 159.36257137727895)
        self.assertEqual(allocation[bidder_ids[2]]['value'], 7.151543249868508)
        self.assertEqual(allocation[bidder_ids[3]]['value'], 142.94765881000774)
        self.assertEqual(allocation[bidder_ids[4]]['value'], 0)
        self.assertEqual(allocation[bidder_ids[5]]['value'], 91.18130341220245)
        self.assertEqual(allocation[bidder_ids[6]]['value'], 9.00418233442389)

    def test_gsvm_bid_seeds(self):
        instance_seed=2
        gsvm = self.pysats.create_gsvm(seed=instance_seed, isLegacyGSVM=False)
        print('Seed:', instance_seed)
        bidder_ids = gsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            # Generate some bids
            bids = gsvm.get_random_bids(bidder_id, 10, seed=123)
            new_bids = gsvm.get_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)
            # Generate some bids with the new method
            bids = gsvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            new_bids = gsvm.get_uniform_random_bids(bidder_id, 10, seed=123)
            self.assertEqual(bids, new_bids)

    def test_multi_instance(self):
        instance_seed = 111
        gsvm = self.pysats.create_gsvm(seed=instance_seed, isLegacyGSVM=False)
        print('Seed:', instance_seed)
        bidder_ids = gsvm.get_bidder_ids()
        for bidder_id in bidder_ids:
            print('Bidder: ', bidder_id)
        self.assertEqual(len(bidder_ids), 7)

    def test_goods_of_interest(self):
        instance_seed = 222
        gsvm = self.pysats.create_gsvm(seed=instance_seed, isLegacyGSVM=False)
        print('Seed:', instance_seed)
        for bidder_id in gsvm.get_bidder_ids():
            goods_of_interest = gsvm.get_goods_of_interest(bidder_id)
            print(f'{gsvm.population[bidder_id].getName()}: {goods_of_interest}')


if __name__ == '__main__':
    unittest.main()
