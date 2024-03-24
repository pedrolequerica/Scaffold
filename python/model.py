from HistoricalChainlinkData import HistoricalChainlinkData
import datetime
from config import *
import  math
from sklearn import linear_model
import statsmodels.api as sm

class Model():

    def __init__(self,features, test, range):
        self.features = features
        self.results = test
        self.range = range
        pass

    def train(self):
        historicalData = HistoricalChainlinkData(abi = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]', rpc='https://rpc.ankr.com/eth_sepolia',metrics=dict(self.features,**self.results))
        historicalData.start_gathering()
        historicalData = historicalData.data
        print(historicalData)
        tend = datetime.datetime.now()
        tstart = datetime.datetime.now() - datetime.timedelta(days=self.range)
        interval = datetime.timedelta(minutes=30)
        periods = []
        period_start = tstart
        while period_start < tend:
            period_end = min(period_start + interval, tend)
            periods.append((period_start, period_end))
            period_start = period_end
        times = []
        #split, then rejoin on common times
        for idx,row in historicalData.iterrows():
            time = row['Date']
            time_strp = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            found = False
            for period in periods:
                if period[0] < time_strp < period[1]:
                    time = periods.index(period)
                    times.append(time)
                    found = True
                else:
                    continue
            if found == False:
                times.append(math.nan)
        historicalData['Date'] = times
        historicalData.dropna(inplace=True)
        print(historicalData)
        self.mv_regress(historicalData)

    @staticmethod
    def mv_regress(historicalData):
        train_test_split=0.7
        print(type(historicalData))
        print([list(features.keys())])

        X = historicalData[[list(features.keys())]]
        Y = historicalData[list(results.keys())]
        X_train = X[0:round(train_test_split*len(X))]
        Y_train = Y[0:round(train_test_split*len(Y))]
        X_test = X[round(train_test_split*len(X)) + 1:-1]
        Y_test = Y[round(train_test_split*len(Y)) + 1:-1]
        regr = linear_model.LinearRegression()
        regr.fit(X_train, Y_train)
        print('Intercept: \n', regr.intercept_)
        print('Coefficients: \n', regr.coef_)


    def test(self):
        pass

def main():
    model = Model(features,results,30)
    model.train()

if __name__ == '__main__':
    main()