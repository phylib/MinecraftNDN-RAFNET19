from change_statistics import IntervalDataSink


class IntervalPrinter(IntervalDataSink.IntervalDataSink):

    def __init__(self):
        super(IntervalPrinter, self).__init__()


    def receiveIntervalData(self, intervalData):
        for entry in intervalData.entries:
            print(entry)
        print('')


    def noMoreIntervals(self):
       print('noMoreIntervals, goodbye!')