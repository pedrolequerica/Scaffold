# THIS IS EXAMPLE CODE THAT USES HARDCODED VALUES FOR CLARITY.
# THIS IS EXAMPLE CODE THAT USES UN-AUDITED CODE.
# DO NOT USE THIS CODE IN PRODUCTION.

from web3 import Web3
import numpy
import sys
import pandas
from time import strftime, localtime

# AggregatorV3Interface ABI
# Feed address
addr = '0x1b44F3514812d835EB1BDB0acB33d3fA3351Ee43'

class HistoricalChainlinkData():
    def __init__(self, abi,rpc,metrics):
        self.web3 = Web3(Web3.HTTPProvider(rpc)) #rpc
        self.data = pandas.DataFrame(columns=['Date', 'Metric', 'Value'])
        self.abi = abi
        self.metrics = metrics

    def start_gathering(self):
        for metric,addr in self.metrics.items():
            self.contract = self.web3.eth.contract(address=addr, abi=self.abi)
            historicalRound = self.contract.functions.latestRoundData().call()[0]
            print(f'Most recent round for metric {metric} as : {historicalRound}')
            roundId =  historicalRound
            self.iterate_through_phase( roundId,metric)

    def iterate_through_phase(self,roundId,metric):
        phaseId = numpy.int64(roundId >> 64)
        print(f'Got phase id as {phaseId}')
        agg_round_id = self.calc_agg_round_id(phaseId)
        i = 0
        round_start = []
        values =[]
        metric_data = pandas.DataFrame(columns=['Date', 'Metric','Value'])
        while (roundId - agg_round_id + i) <= roundId:
            print(f'investigating metrics from round {roundId}')
            round_data = self.contract.functions.getRoundData(roundId).call()
            values.append(round_data[1])
            round_start.append(round_data[3])
            i+=1
        metric_data['Metric'] = [metric] * len(values)
        metric_data['Value'] = values
        metric_data['Date'] = [strftime('%Y-%m-%d %H:%M:%S', localtime(timest)) for timest in round_start]
        self.data = pandas.concat([self.data, metric_data])

    def calc_agg_round_id(self,phaseId):
        phaseId_as_int64 = numpy.int64(phaseId)
        largest_64_bit = numpy.int64(sys.maxsize)
        agg_round_id = phaseId_as_int64 & largest_64_bit
        print(f'Calculated agg_round_id as {agg_round_id}')
        return agg_round_id

if __name__ == '__main__':
    main()
