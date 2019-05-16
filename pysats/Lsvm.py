from jnius import JavaClass, MetaJavaClass, JavaMethod, JavaMultipleMethod, cast, autoclass

SizeBasedUniqueRandomXOR = autoclass(
    'org.spectrumauctions.sats.core.bidlang.xor.SizeBasedUniqueRandomXOR')
JavaUtilRNGSupplier = autoclass(
    'org.spectrumauctions.sats.core.util.random.JavaUtilRNGSupplier')
Bundle = autoclass(
    'org.spectrumauctions.sats.core.model.Bundle')
LSVMStandardMIP = autoclass(
    'org.spectrumauctions.sats.opt.model.lsvm.LSVMStandardMIP')

class _Lsvm(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'org/spectrumauctions/sats/core/model/lsvm/LocalSynergyValueModel'

    # TODO: I don't find a way to have the more direct accessors of the DefaultModel class. So for now, I'm mirroring the accessors 
    #createNewPopulation = JavaMultipleMethod([
    #    '()Ljava/util/List;',
    #    '(J)Ljava/util/List;'])
    setNumberOfNationalBidders = JavaMethod('(I)V')
    setNumberOfRegionalBidders = JavaMethod('(I)V')
    createWorld = JavaMethod(
        '(Lorg/spectrumauctions/sats/core/util/random/RNGSupplier;)Lorg/spectrumauctions/sats/core/model/lsvm/LSVMWorld;')
    createPopulation = JavaMethod(
        '(Lorg/spectrumauctions/sats/core/model/World;Lorg/spectrumauctions/sats/core/util/random/RNGSupplier;)Ljava/util/List;')

    population = {}
    goods = {}
    efficient_allocation = None

    def __init__(self, seed, number_of_national_bidders, number_of_regional_bidders):
        super().__init__()
        if seed:
            rng = JavaUtilRNGSupplier(seed)
        else:
            rng = JavaUtilRNGSupplier()

        self.setNumberOfNationalBidders(number_of_national_bidders)
        self.setNumberOfNationalBidders(number_of_regional_bidders)
        
        world = self.createWorld(rng)
        self._bidder_list = self.createPopulation(world, rng)

        # Store bidders
        bidderator = self._bidder_list.iterator()
        while bidderator.hasNext():
            bidder = bidderator.next()
            self.population[bidder.getId()] = bidder
        
        # Store goods
        goods_iterator = self._bidder_list.iterator().next().getWorld().getLicenses().iterator()
        count = 0
        while goods_iterator.hasNext():
            good = goods_iterator.next()
            assert good.getId() == count
            count += 1
            self.goods[good.getId()] = good
        
    
    def get_bidder_ids(self):
        return self.population.keys()

    def get_good_ids(self):
        return self.goods.keys()

    def calculate_value(self, bidder_id, goods_vector):
        assert len(goods_vector) == len(self.goods.keys())
        bidder = self.population[bidder_id]
        bundle = Bundle()
        for i in range(len(goods_vector)):
            if goods_vector[i] == 1:
                bundle.add(self.goods[i])
        return bidder.calculateValue(bundle).doubleValue()
    
    def get_random_bids(self, bidder_id, number_of_bids, mean_bundle_size=3, standard_deviation_bundle_size=2):
        bidder = self.population[bidder_id]
        valueFunction = cast('org.spectrumauctions.sats.core.bidlang.xor.SizeBasedUniqueRandomXOR',
                                bidder.getValueFunction(SizeBasedUniqueRandomXOR))
        valueFunction.setDistribution(
            mean_bundle_size, standard_deviation_bundle_size)
        valueFunction.setIterations(number_of_bids)
        xorBidIterator = valueFunction.iterator()
        bids = []
        while (xorBidIterator.hasNext()):
            xorBid = xorBidIterator.next()
            bid = []
            for good_id, good in self.goods.items():
                if (xorBid.getLicenses().contains(good)):
                    bid.append(1)
                else:
                    bid.append(0)
            bid.append(xorBid.value)
            bids.append(bid)
        return bids

    def get_efficient_allocation(self):
        if self.efficient_allocation:
            return self.efficient_allocation
        
        mip = LSVMStandardMIP(self._bidder_list)
        mip.setDisplayOutput(True)
        
        item_allocation = cast('org.spectrumauctions.sats.opt.domain.ItemAllocation', mip.calculateAllocation())
        
        self.efficient_allocation = {}

        for bidder_id, bidder in self.population.items():
            self.efficient_allocation[bidder_id] = {}
            self.efficient_allocation[bidder_id]['good_ids'] = []
            bidder_allocation = item_allocation.getAllocation(bidder)
            good_iterator = bidder_allocation.iterator()
            while good_iterator.hasNext():
                self.efficient_allocation[bidder_id]['good_ids'].append(good_iterator.next().getId())

            self.efficient_allocation[bidder_id]['value'] = item_allocation.getTradeValue(bidder).doubleValue()
        
        return self.efficient_allocation, item_allocation.totalValue.doubleValue()
