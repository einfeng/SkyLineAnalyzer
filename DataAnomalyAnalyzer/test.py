
import pandas
import numpy

data = [5,4,5,6,7,6,4,8,4,5,3,6,10,10,10,10,10,10,10,30,30,30,30,-35]

series = pandas.Series(data)
median = series.median()


demedianed = numpy.abs(series - median)
median_deviation = demedianed.median()


# The test statistic is infinite when the median is zero,
# so it becomes super sensitive. We play it safe and skip when this happens.
result = False

if median_deviation == 0:
    result = False

test_statistic = demedianed.iget(-1) / median_deviation

print('median:'+str(median))

print('median_deviation:'+str(median_deviation))
print('demedianed.iget(-1):'+str(demedianed.iget(-1)))
print('test_statistic:'+str(test_statistic))

if test_statistic > 6:
    result =  True
    
print('result:'+str(result))