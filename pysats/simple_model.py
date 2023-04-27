from jnius import (
    JavaClass,
    MetaJavaClass,
    JavaMethod,
    JavaMultipleMethod,
    cast,
    autoclass,
)

SizeBasedUniqueRandomXOR = autoclass(
    "org.spectrumauctions.sats.core.bidlang.xor.SizeBasedUniqueRandomXOR"
)
JavaUtilRNGSupplier = autoclass(
    "org.spectrumauctions.sats.core.util.random.JavaUtilRNGSupplier"
)
Random = autoclass("java.util.Random")
HashSet = autoclass("java.util.HashSet")
LinkedList = autoclass("java.util.LinkedList")
Bundle = autoclass("org.marketdesignresearch.mechlib.core.Bundle")
BundleEntry = autoclass("org.marketdesignresearch.mechlib.core.BundleEntry")
InstanceHandler = autoclass(
    "org.spectrumauctions.sats.core.util.instancehandling.InstanceHandler"
)
InMemoryInstanceHandler = autoclass(
    "org.spectrumauctions.sats.core.util.instancehandling.InMemoryInstanceHandler"
)
JSONInstanceHandler = autoclass(
    "org.spectrumauctions.sats.core.util.instancehandling.JSONInstanceHandler"
)
LinkedHashMap = autoclass("java.util.LinkedHashMap")
Price = autoclass("org.marketdesignresearch.mechlib.core.price.Price")
LinearPrices = autoclass("org.marketdesignresearch.mechlib.core.price.LinearPrices")


class SimpleModel(JavaClass):
    def __init__(self, seed, mip_path: str, store_files=False):
        super().__init__()
        if seed:
            rng = JavaUtilRNGSupplier(seed)
        else:
            rng = JavaUtilRNGSupplier()

        self.population = {}
        self.goods = {}
        self.mip_path = mip_path
        self.efficient_allocation = None
        # The following sets the instance handler to InMemory (i.e., no files are stored), if store_files is false
        # Note that since InstanceHandler is a singleton, if you're running experiments in parallel, it may lead
        # to troubles to have this flag set to True in one experiment and False in another one. This is best used
        # in a consistent way, which is probably the idea anyway in most cases.
        InstanceHandler.setDefaultHandler(
            JSONInstanceHandler.getInstance()
            if store_files
            else InMemoryInstanceHandler.getInstance()
        )
        self.prepare_world()
        world = self.createWorld(rng)
        self._bidder_list = self.createPopulation(world, rng)

        # Store bidders
        bidderator = self._bidder_list.iterator()
        count = 0
        while bidderator.hasNext():
            bidder = bidderator.next()
            self.population[count] = bidder
            count += 1

        # Store goods
        goods_iterator = world.getLicenses().iterator()
        count = 0
        while goods_iterator.hasNext():
            good = goods_iterator.next()
            assert good.getLongId() == count
            count += 1
            self.goods[good.getLongId()] = good

        # Python maintains insertion order since 3.7, so it's fine to fill these dictionaries this way
        # -> https://stackoverflow.com/a/40007169

    def prepare_world(self):
        """
        Here, child classes will set the parameters for the world creation, e.g. the
        number of bidders
        """
        raise NotImplementedError("Child class has to implement this method")

    def get_model_name(self):
        raise NotImplementedError("Child class has to implement this method")

    def get_bidder_ids(self):
        return list(self.population.keys())

    def get_good_ids(self):
        return list(self.goods.keys())

    def calculate_value(self, bidder_id, goods_vector):
        bidder = self.population[bidder_id]
        bundle = self._vector_to_bundle(goods_vector)
        return bidder.calculateValue(bundle).doubleValue()

    def calculate_values(self, bidder_id, goods_vector_2D):
        bidder = self.population[bidder_id]
        bundles = LinkedList()
        for goods_vector in goods_vector_2D:
            bundle = self._vector_to_bundle(goods_vector)
            bundles.add(bundle)
        return [x.doubleValue() for x in bidder.calculateValues(bundles)]

    def get_best_bundles(
        self, bidder_id, price_vector, max_number_of_bundles, allow_negative=False
    ):
        assert len(price_vector) == len(self.goods.keys())
        bidder = self.population[bidder_id]
        prices_map = LinkedHashMap()
        index = 0
        for good in self.goods.values():
            prices_map.put(good, Price.of(price_vector[index]))
            index += 1
        bundles = bidder.getBestBundles(
            LinearPrices(prices_map), max_number_of_bundles, allow_negative
        )
        result = []
        for bundle in bundles:
            assert bundle.areSingleQuantityGoods()
            bundle_vector = []
            for i in range(len(price_vector)):
                if bundle.contains(self.goods[i]):
                    bundle_vector.append(1)
                else:
                    bundle_vector.append(0)
            result.append(bundle_vector)
        return result

    def get_goods_of_interest(self, bidder_id):
        bidder = self.population[bidder_id]
        goods_of_interest = []
        for good_id, good in self.goods.items():
            good_set = HashSet()
            good_set.add(good)
            bundle = Bundle.of(good_set)
            if bidder.getValue(bundle, True).doubleValue() > 0:
                goods_of_interest.append(good_id)
        return goods_of_interest

    def get_uniform_random_bids(self, bidder_id, number_of_bids, seed=None):
        bidder = self.population[bidder_id]
        goods = LinkedList()
        for good in self.goods.values():
            goods.add(good)
        if seed:
            random = Random(seed)
        else:
            random = Random()

        bids = []
        for i in range(number_of_bids):
            bid = []
            bundle = bidder.getAllocationLimit().getUniformRandomBundle(random, goods)
            for good_id, good in self.goods.items():
                if bundle.contains(good):
                    bid.append(1)
                else:
                    bid.append(0)
            bid.append(bidder.getValue(bundle).doubleValue())
            bids.append(bid)
        return bids

    def get_random_bids(
        self,
        bidder_id,
        number_of_bids,
        seed=None,
        mean_bundle_size=9,
        standard_deviation_bundle_size=4.5,
    ):
        bidder = self.population[bidder_id]
        if seed:
            rng = JavaUtilRNGSupplier(seed)
        else:
            rng = JavaUtilRNGSupplier()
        valueFunction = cast(
            "org.spectrumauctions.sats.core.bidlang.xor.SizeBasedUniqueRandomXOR",
            bidder.getValueFunction(SizeBasedUniqueRandomXOR, rng),
        )
        valueFunction.setDistribution(mean_bundle_size, standard_deviation_bundle_size)
        valueFunction.setIterations(number_of_bids)
        xorBidIterator = valueFunction.iterator()
        bids = []
        while xorBidIterator.hasNext():
            bundleValue = xorBidIterator.next()
            bid = []
            for good_id, good in self.goods.items():
                if bundleValue.getBundle().contains(good):
                    bid.append(1)
                else:
                    bid.append(0)
            bid.append(bundleValue.getAmount().doubleValue())
            bids.append(bid)
        return bids

    def get_efficient_allocation(self, display_output=False):
        if self.efficient_allocation:
            return self.efficient_allocation, sum(
                [
                    self.efficient_allocation[bidder_id]["value"]
                    for bidder_id in self.efficient_allocation.keys()
                ]
            )

        mip = autoclass(self.mip_path)(self._bidder_list)
        mip.setDisplayOutput(display_output)

        allocation = mip.calculateAllocation()

        self.efficient_allocation = {}

        for bidder_id, bidder in self.population.items():
            self.efficient_allocation[bidder_id] = {}
            self.efficient_allocation[bidder_id]["good_ids"] = []
            bidder_allocation = allocation.allocationOf(bidder)
            good_iterator = (
                bidder_allocation.getBundle().getSingleQuantityGoods().iterator()
            )
            while good_iterator.hasNext():
                self.efficient_allocation[bidder_id]["good_ids"].append(
                    good_iterator.next().getLongId()
                )

            self.efficient_allocation[bidder_id][
                "value"
            ] = bidder_allocation.getValue().doubleValue()

        return (
            self.efficient_allocation,
            allocation.getTotalAllocationValue().doubleValue(),
        )

    def _vector_to_bundle(self, vector):
        assert len(vector) == len(self.goods.keys())
        bundleEntries = HashSet()
        for i in range(len(vector)):
            if vector[i] == 1:
                bundleEntries.add(BundleEntry(self.goods[i], 1))
        return Bundle(bundleEntries)
