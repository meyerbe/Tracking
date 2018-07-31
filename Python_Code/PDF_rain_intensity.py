import os, sys
# import argparse
# import json as simplejson
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm
import glob
import ntpath

from PDF_plotting_functions import plot_scatter_daily, plot_histogram_daily
from PDF_plotting_functions import plot_histogram_4hourly

def main():
    print('main')

    # path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/RADAR_ESTIMATED_RAIN_RATE'
    path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/RADAR_ESTIMATED_RAIN_RATE_test'
    files = [name for name in os.listdir(path_data) if name[-2:]=='nc']
    n_files = len([name for name in os.listdir(path_data) if name[-2:]=='nc'])
    print('# files: ' + np.str(n_files))
    print('')

    ''' Read in test file '''
    path_in = os.path.join(path_data, files[0])
    rootgrp = nc.Dataset(path_in, 'r')
    var = rootgrp.variables['radar_estimated_rain_rate']
    dim = var.shape
    n_time = var.shape[0]
    long = var.shape[1]
    lat = var.shape[2]
    rootgrp.close()

    # define data structures for PDFs
    # for (2)
    mean = np.zeros(shape=(n_files))
    variance = np.zeros(shape=(n_files))
    max = np.zeros(shape=(n_files))
    date_list = []

    index = 0

    # num_bins = 200
    bin_arr = np.append(np.append(np.arange(0,10,0.1),np.arange(10,100,1)), np.arange(100,201,10))
    bin_arr = np.append(np.append(np.arange(0,50,0.1),np.arange(50,100,1)), np.arange(100,201,10))
    bin_arr_large = np.arange(0,201,1)
    bin_arr_test = np.arange(0,110,10)
    for path_in in glob.glob(os.path.join(path_data, '*')):
        data_name = ntpath.basename(path_in)[:-3]
        date = data_name[-8:]
        date_list.append(date)
        print('name: ', data_name)
        # print('path:', path_in)

        ''' Read in radar data file '''
        rootgrp = nc.Dataset(path_in, 'r')
        var = rootgrp.variables['radar_estimated_rain_rate']
        if var.shape != dim:
            print('Problem in time steps: break')
            break
        data_rr = np.ndarray(shape=var.shape)
        data_rr = var[:]
        rootgrp.close()
        data = np.ravel(data_rr)

        ''' (1) Histogram from 4-hourly data '''
        if index == 0:
            hist, bin_edges = np.histogram(data, bins=bin_arr, normed=False)
            hist_test, bin_edges_test = np.histogram(data, bins=bin_arr_test, normed=False)
            # hist_l, bin_edges_l = np.histogram(data, bins=bin_arr_large, normed=False)
        else:
            hist += np.histogram(data, bins=bin_arr, normed=False)[0]
            hist_test += np.histogram(data, bins=bin_arr_test, normed=False)[0]
            # hist_l += np.histogram(data, bins=bin_arr_large, normed=False)[0]

        ''' (2) Statistics / Histogram of daily mean '''
        mean[index] = np.mean(data)
        variance[index] = np.var(data)
        max[index] = np.amax(data)


        index += 1


    # ???? for 2001-2003: hist[0]<hist[1], hist[2]<hist[1] ???? why not first component the largest???

    ''' (1) plotting 4-hourly mean '''
    # hist:         array with number of points that fall in the bins defined by bin_arr (np.shape(hist) = np.shape(bin_arr))
    # hist[0] ~ 95.7% of cumulated points (np.sum(hist[:]))
    # hist[1] ~ 0.84% of cumulated points (np.sum(hist[:])); 19.4% of cumulated points from 1 (np.sum(hist[1:]))
    # hist[2] ~ 0.5% of cumulated points (np.sum(hist[:]))

    # hist_test:
    # bin_arr_test = np.arange(0,110,10) = [0, 10, ..., 100]
    # hist_test:     array of length 10 with 99.6% of points in first bin (0 < rr < 10)
    # print('')
    # print('bin arr test', bin_arr_test)

    print('')
    print('hist:', hist.shape, type(hist), hist[0], hist[1], hist[2])
    print('hist[0]:', np.double(hist[0])/np.sum(hist))
    print('hist[1]:', np.double(hist[1])/np.sum(hist), np.double(hist[1])/np.sum(hist[1:]))
    print('hist[2]:', np.double(hist[2])/np.sum(hist), np.double(hist[2])/np.sum(hist[1:]))
    print('')

    ''' (1a) computing percentiles '''
    # arr_per:        array with percentiles and the index of the correspondind bins (incl. / excl. first bin)
    # arr_per[0]:     percentiles
    # arr_per[1]:     number of points in that percentile
    # arr_per[2]:     index of bin into which the percentile falls (incl. the first bin)
    # arr_per[3]:     index of bin into which the percentile falls (excl. the first bin)
    per_arr = np.asarray([10,20,50,75,90,95,96,97,98,99,99.9], dtype=np.double)
    n_per = per_arr.shape[0]
    per_arr = np.append(per_arr, 0.01*np.sum(hist)*per_arr).reshape(2,n_per)
    per_arr = np.append(per_arr, np.zeros(shape=per_arr.shape[1])).reshape(3,n_per)
    per_arr = np.append(per_arr, np.zeros(shape=per_arr.shape[1])).reshape(4,n_per)

    print('cum: ', np.sum(hist), 'hist[0]:', hist[0], 'hist[1]:', hist[1])
    for ip, per in enumerate(per_arr[1,:]):
        # per = np.percentile(hist, p)
        print(
        'percentile ' + np.str(per_arr[0, ip]) + '%: ' + np.str(np.int(per)))
        i = 0
        cum = hist[i]
        while (cum < per):

            i += 1
            cum += hist[i]
            # print('cum', cum, 'percentile', per, 'i', i)
        print('cum[-1]=' + np.str(np.sum(hist[:i])), 'cum=' + np.str(np.sum(hist[:i + 1])), 'i=' + np.str(i))
        per_arr[2,ip] = i
    print('')

    per_arr_ = 0.01 * np.sum(hist[1:]) * per_arr[0,:]
    for ip, per in enumerate(per_arr_):
        # per_1 = np.percentile(hist[1:], p)
        i = 1
        cum = hist[1]
        while (cum < per):
            i += 1
            cum += hist[i]
        per_arr[3,ip] = i
        print('_percentile ' + np.str(per_arr[0,ip]) + '%: ' + np.str(np.int(per)), 'cum=' + np.str(np.sum(hist[:i + 1])),
              'i=' + np.str(i))


    bin_max = 100
    plot_histogram_4hourly(hist, bin_arr, bin_max, per_arr, date_list, n_files, n_time, lat, long)



    ''' (2) plotting daily mean '''
    meanmean = np.mean(mean)
    varmean = np.var(mean)
    extremes = []
    for i,f in enumerate(files):
        if mean[i] > (meanmean+2*varmean) or mean[i] < (meanmean-2*varmean):
            extremes.append([i, mean[i], f[-11:-3]])
    plot_scatter_daily(mean, variance, max, meanmean, varmean, extremes, date_list)
    plot_histogram_daily(mean, variance, meanmean, varmean, extremes, date_list)


    return


# # ----------------------------------------------------------------------
# def read_in_netcdf(variable_name, fullpath_in):
#     rootgrp = nc.Dataset(fullpath_in, 'r')
#     var = rootgrp.groups['fields'].variables[variable_name]
#
#     shape = var.shape
#     print('shape:', var.shape)
#     data = np.ndarray(shape=var.shape)
#     data = var[:]
#     rootgrp.close()
#     return data

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()

