from jnius import JavaClass, MetaJavaClass, JavaMethod, JavaMultipleMethod, cast, autoclass

SizeBasedUniqueRandomXOR = autoclass(
    'org.spectrumauctions.sats.core.bidlang.xor.SizeBasedUniqueRandomXOR')
JavaUtilRNGSupplier = autoclass(
    'org.spectrumauctions.sats.core.util.random.JavaUtilRNGSupplier')
Bundle = autoclass(
    'org.spectrumauctions.sats.core.model.Bundle')

MRVM_MIP = autoclass(
    'org.spectrumauctions.sats.opt.model.mrvm.MRVM_MIP')

class _Mrvm(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'org/spectrumauctions/sats/core/model/mrvm/MultiRegionModel'

    # TODO: I don't find a way to have the more direct accessors of the DefaultModel class. So for now, I'm mirroring the accessors 
    #createNewPopulation = JavaMultipleMethod([
    #    '()Ljava/util/List;',
    #    '(J)Ljava/util/List;'])
    setNumberOfNationalBidders = JavaMethod('(I)V')
    setNumberOfRegionalBidders = JavaMethod('(I)V')
    setNumberOfLocalBidders = JavaMethod('(I)V')
    createWorld = JavaMethod(
        '(Lorg/spectrumauctions/sats/core/util/random/RNGSupplier;)Lorg/spectrumauctions/sats/core/model/mrvm/MRVMWorld;')
    createPopulation = JavaMethod(
        '(Lorg/spectrumauctions/sats/core/model/World;Lorg/spectrumauctions/sats/core/util/random/RNGSupplier;)Ljava/util/List;')

    population = {}
    goods = {}
    efficient_allocation = None

    def __init__(self, seed, number_of_national_bidders, number_of_regional_bidders, number_of_local_bidders):
        super().__init__()
        if seed:
            rng = JavaUtilRNGSupplier(seed)
        else:
            rng = JavaUtilRNGSupplier()

        self.setNumberOfNationalBidders(number_of_national_bidders)
        self.setNumberOfRegionalBidders(number_of_regional_bidders)
        self.setNumberOfLocalBidders(number_of_local_bidders)
        
        world = self.createWorld(rng)
        self._bidder_list = self.createPopulation(world, rng)

        # Store bidders
        bidderator = self._bidder_list.iterator()
        while bidderator.hasNext():
            bidder = bidderator.next()
            self.population[bidder.getId()] = bidder
        
        # Store goods
        goods_iterator = self._bidder_list.iterator().next().getWorld().getLicenses().iterator()
        while goods_iterator.hasNext():
            good = goods_iterator.next()
            self.goods[good.getId()] = good

        self.goods = list(map(lambda _id: self.goods[_id], sorted(self.goods.keys())))
    
    def get_bidder_ids(self):
        return self.population.keys()

    def calculate_value(self, bidder_id, goods_vector):
        assert len(goods_vector) == len(self.goods)
        bidder = self.population[bidder_id]
        bundle = Bundle()
        for i in range(len(goods_vector)):
            if goods_vector[i] == 1:
                bundle.add(self.goods[i])
        return bidder.calculateValue(bundle).doubleValue()
    
    def get_random_bids(self, bidder_id, number_of_bids, seed=None, mean_bundle_size=49, standard_deviation_bundle_size=24.5):
        bidder = self.population[bidder_id]
        if seed:
            rng = JavaUtilRNGSupplier(seed)
        else:
            rng = JavaUtilRNGSupplier()
        valueFunction = cast('org.spectrumauctions.sats.core.bidlang.xor.SizeBasedUniqueRandomXOR',
                                bidder.getValueFunction(SizeBasedUniqueRandomXOR, rng))
        valueFunction.setDistribution(
            mean_bundle_size, standard_deviation_bundle_size)
        valueFunction.setIterations(number_of_bids)
        xorBidIterator = valueFunction.iterator()
        bids = []
        while (xorBidIterator.hasNext()):
            xorBid = xorBidIterator.next()
            bid = []
            for i in range(len(self.goods)):
                if (xorBid.getLicenses().contains(self.goods[i])):
                    bid.append(1)
                else:
                    bid.append(0)
            bid.append(xorBid.value)
            bids.append(bid)
        return bids

    def get_efficient_allocation(self):
        if self.efficient_allocation:
            return self.efficient_allocation
        
        mip = MRVM_MIP(self._bidder_list)
        mip.setDisplayOutput(True)
        
        generic_allocation = cast(
            'org.spectrumauctions.sats.opt.domain.GenericAllocation', mip.calculateAllocation())
        
        self.efficient_allocation = {}

        for bidder_id, bidder in self.population.items():
            self.efficient_allocation[bidder_id] = {}
            self.efficient_allocation[bidder_id]['good_ids'] = []
            if generic_allocation.getWinners().contains(bidder):
                bidder_allocation = generic_allocation.getAllocation(bidder)
                good_iterator = bidder_allocation.iterator()
                while good_iterator.hasNext():
                    self.efficient_allocation[bidder_id]['good_ids'].append(good_iterator.next().getId())

            self.efficient_allocation[bidder_id]['value'] = generic_allocation.getTradeValue(
                bidder).doubleValue()
        
        return self.efficient_allocation, generic_allocation.totalValue.doubleValue()
