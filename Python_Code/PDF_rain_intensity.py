import os, sys
# import argparse
# import json as simplejson
import numpy as np
# import pylab as plt
import netCDF4 as nc
# from matplotlib.colors import LogNorm
import glob
import ntpath

from PDF_plotting_functions import plot_scatter_all, plot_histogram_all

def main():
    print('main')

    # path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/RADAR_ESTIMATED_RAIN_RATE'
    path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/RADAR_ESTIMATED_RAIN_RATE_test'
    files = [name for name in os.listdir(path_data) if name[-2:]=='nc']
    # print(files)
    # print(type(files))
    n_files = len([name for name in os.listdir(path_data) if name[-2:]=='nc'])
    print('# files: ' + np.str(n_files))
    print('')

    # y = 2002; m = 1; d = 1
    # date = np.str(y*10000 + m*100 + d)
    # file_name = 'CPOL_RADAR_ESTIMATED_RAIN_RATE_' + date + '.nc'
    # path_in = os.path.join(path_data, file_name)
    # # var_name = 'radar_estimated_rain_rate'

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
    date_list = []

    index = 0
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

        # # (1) PDF from all data
        # aux = np.zeros(shape=(data1.shape[0] - data2.shape[0], nz))
        # data_all = np.append(data_all, aux, axis=0)
        # print('shapes', data1.shape, data2.shape)
        # print('')
        # del aux

        # (2) PDF for each day
        data = np.ravel(data_rr)
        # print(data.size, data.shape)
        # print(data_rr.size, data_rr.shape)
        mean[index] = np.mean(data)
        variance[index] = np.var(data)


        index += 1

    meanmean = np.mean(mean)
    varmean = np.var(mean)
    extremes = []
    for i,f in enumerate(files):
        if mean[i] > (meanmean+2*varmean) or mean[i] < (meanmean-2*varmean):
            extremes.append([i, mean[i], f[-11:-3]])

    plot_scatter_all(mean, variance, meanmean, varmean, extremes, date_list)

    plot_histogram_all(mean, variance, meanmean, varmean, extremes, date_list)


    return


# ----------------------------------------------------------------------
def read_in_netcdf(variable_name, fullpath_in):
    rootgrp = nc.Dataset(fullpath_in, 'r')
    var = rootgrp.groups['fields'].variables[variable_name]

    shape = var.shape
    print('shape:', var.shape)
    data = np.ndarray(shape=var.shape)
    data = var[:]
    rootgrp.close()
    return data

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()

