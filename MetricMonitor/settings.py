##########oracle setting##########
USER='bomc'
PASSWORD='bomc'
CONNECTSTR='192.168.56.5:1521/wydb'
OCIPATH='D:/instantclient_11_2'



##########program setting##########

# This is the rolling duration that will be stored in Redis. Be sure to pick a
# value that suits your memory capacity, your CPU capacity, and your overall
# metrics count. Longer durations take a longer to analyze, but they can
# help the algorithms reduce the noise and provide more accurate anomaly
# detection.

FULL_DURATION = 86400

# This is the duration, in seconds, for a metric to become 'stale' and for
# the analyzer to ignore it until new datapoints are added. 'Staleness' means
# that a datapoint has not been added for STALE_PERIOD seconds.

STALE_PERIOD = 500000000

# This is the minimum length of a timeseries, in datapoints, for the analyzer
# to recognize it as a complete series.

MIN_TOLERABLE_LENGTH = 1

# Sometimes a metric will continually transmit the same number. There's no need
# to analyze metrics that remain boring like this, so this setting determines
# the amount of boring datapoints that will be allowed to accumulate before the
# analyzer skips over the metric. If the metric becomes noisy again, the
# analyzer will stop ignoring it.

MAX_TOLERABLE_BOREDOM = 1000

# By default, the analyzer skips a metric if it it has transmitted a single
# number MAX_TOLERABLE_BOREDOM times. Change this setting if you wish the size
# of the ignored set to be higher (ie, ignore the metric if there have only
# been two different values for the past MAX_TOLERABLE_BOREDOM datapoints).
# This is useful for timeseries that often oscillate between two values.

BOREDOM_SET_SIZE = 2


# These are the algorithms that the Analyzer will run. To add a new algorithm,
# you must both define the algorithm in algorithms.py and add its name here.

ALGORITHMS = [
    'first_hour_average',
    'mean_subtraction_cumulation',
    'stddev_from_average',
    'stddev_from_moving_average',
    'least_squares',
    'grubbs',
    'histogram_bins',
    'median_absolute_deviation',
    'ks_test',
]

# This is the number of algorithms that must return True before a metric is
# classified as anomalous.
CONSENSUS = 4

