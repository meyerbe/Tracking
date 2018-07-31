import numpy as np
# import pylab as plt
import matplotlib
import matplotlib.pyplot as plt
import scipy
from scipy import stats

def plot_scatter_daily(mean, variance, max, meanmean, varmean, extremes, dates):

    print('plotting')

    # Now switch to a more OO interface to exercise more features.
    # fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(20,9))
    plt.figure(figsize=(30,9))
    # fig, axs = plt.subplots(nrows=1, ncols=2, sharex=False, figsize=(30,9))
    plt.subplot(1,3,1)
    plt.plot(dates, mean, '.')
    for i in range(len(extremes)):
        plt.plot(extremes[i][2], extremes[i][1], '.r')
    plt.plot([dates[0],dates[-1]], [meanmean,meanmean], 'k--', linewidth=1, label='mean(means)')
    plt.plot([dates[0],dates[-1]], [meanmean+varmean,meanmean+varmean], 'k', linewidth=1, label=r'mean(means)$\pm$var(means)')
    plt.plot([dates[0],dates[-1]], [meanmean-varmean,meanmean-varmean], 'k', linewidth=1)
    plt.plot([dates[0],dates[-1]], [meanmean+2*varmean,meanmean+2*varmean], '0.75', linewidth=1, label=r'mean(means)$\pm$2*var(means)')
    plt.plot([dates[0],dates[-1]], [meanmean-2*varmean,meanmean-2*varmean], '0.75', linewidth=1)
    plt.title('mean rain rates')
    plt.legend()
    plt.xlabel('dates')
    plt.ylabel('mean (rain rate [mm/h])')

    plt.subplot(1,3,2)
    plt.errorbar(dates, mean, yerr=variance, fmt='o')#, color='b')
    # ax.errorbar(extremes[:][2], extremes[:][1], yerr=variance, fmt='o', color='r')
    # ax.errorbar(extremes[:][2], extremes[:][1], fmt='o', color='r')
    for i in range(len(extremes)):
        plt.errorbar(extremes[i][2], extremes[i][1], fmt='o', color='r')
    plt.plot([dates[0], dates[-1]], [meanmean + varmean, meanmean + varmean], 'k', linewidth=1)
    plt.plot([dates[0], dates[-1]], [meanmean - varmean, meanmean - varmean], 'k', linewidth=1)
    plt.title('mean + var')
    plt.xlabel('dates')
    plt.ylabel('mean (rain rate [mm/h])')
    plt.savefig('./alldata_mean_var.png')

    plt.subplot(1,3,3)
    plt.errorbar(dates, mean, yerr=variance, fmt='o', label=r'daily mean$\pm$var')#, color='b')
    for i in range(len(extremes)):
        if i == 0:
            plt.errorbar(extremes[i][2], extremes[i][1], fmt='o', color='r', label='extremes')
        else:
            plt.errorbar(extremes[i][2], extremes[i][1], fmt='o', color='r')
    plt.plot(dates, max, '.-', label='daily max values')  # , '.-', '0.4', label='daily max values')
    plt.plot([dates[0], dates[-1]], [meanmean + varmean, meanmean + varmean], 'k', linewidth=1)
    plt.plot([dates[0], dates[-1]], [meanmean - varmean, meanmean - varmean], 'k', linewidth=1)
    plt.legend(loc='best')
    plt.title('mean + var')
    plt.xlabel('dates')
    plt.ylabel('mean (rain rate [mm/h])')

    plt.suptitle('Daily mean rain rates', fontsize=21)
    plt.savefig('./alldata_mean_var.png')
    return



def plot_histogram_daily(mean, variance, meanmean, varmean, extremes, date_list):

    import matplotlib.mlab as mlab

    print('plot histogram')


    plt.figure(figsize=(20,9))
    plt.subplot(1,2,1)
    num_bins = 20
    n, bins, patches = plt.hist(mean, num_bins, density=False, facecolor='green', alpha=0.5)
    plt.xlabel('mean (rain rate [mm/h])')
    plt.ylabel('p(mean)')
    plt.title('all dates, unnormed')

    plt.subplot(1,2,2)
    num_bins = 50
    n, bins, patches = plt.hist(mean, num_bins, density=True, facecolor='green', alpha=0.5)
    y = scipy.stats.norm.pdf(bins, meanmean, varmean)
    plt.plot(bins, y, 'r--', label='best fit normal distribution')
    plt.legend(loc='best')
    plt.xlabel('mean (rain rate [mm/h])')
    plt.ylabel('p(mean)')
    plt.title('all dates, normed')

    plt.suptitle('Histogram daily mean rain rates', fontsize=21)
    plt.savefig('./alldata_hist_means.png')

    # plt.subplot(1, 3, 3)
    # # add a 'best fit' line
    # # example data
    # mu = 100  # mean of distribution
    # sigma = 15  # standard deviation of distribution
    # x = mu + sigma * np.random.randn(10000)
    # num_bins = 50
    # # the histogram of the data
    # n, bins, patches = plt.hist(x, num_bins, density=True, facecolor='green', alpha=0.5)
    # # add a 'best fit' line
    # y = scipy.stats.norm.pdf(bins, mu, sigma)
    # plt.plot(bins, y, 'r--', label='best fit normal distribution')


    return



def plot_histogram_4hourly(hist, bin_arr, bin_max, per_arr, date_list, n_files, n_time, lat, long):
    cm = plt.cm.get_cmap('gist_rainbow')
    cm_r = plt.cm.get_cmap('gist_rainbow_r')
    n_tot = per_arr.shape[1]

    plt.figure(figsize=(27, 9))
    plt.subplot(1, 3, 1)
    width = 1. * (bin_arr[1] - bin_arr[0])
    center = (bin_arr[:-1] + bin_arr[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.title('(bin-width=0.1)')
    # width = 0.75 * (bin_arr_large[1] - bin_arr_large[0])
    # center = (bin_arr_large[:-1] + bin_arr_large[1:]) / 2
    # plt.bar(center, hist_l, align='center', width=width)
    # plt.title('(bin-width=1.0)')
    plt.ylim([0, hist[2] * 1.001])
    plt.xlabel('rain rate [mm/h]   (4-hourly mean)')
    plt.ylabel('p(rr)')

    plt.subplot(1, 3, 2)
    width = .75 * (bin_arr[1] - bin_arr[0])
    center = (bin_arr[:bin_max] + bin_arr[1:(bin_max + 1)]) / 2
    plt.bar(center, hist[:bin_max], align='center', width=width)
    plt.title('(bin-width=0.1)')
    # width = 0.75 * (bin_arr_large[1] - bin_arr_large[0])
    # center = (bin_arr_large[:-1] + bin_arr_large[1:]) / 2
    # plt.bar(center, hist_l, align='center', width=width)
    # plt.title('(bin-width=1.0)')
    # percentiles:
    for i, ip in enumerate(per_arr[2,:]):
        ip = np.int(ip)
        if ip < bin_max:
            plt.bar(center[ip], hist[ip], align='center', width=width,
                # color = 'r', #
                color=cm_r(np.double(i)/n_tot),
                label=np.str(per_arr[0,i])+'th percentile (i='+np.str(ip)+')')
    plt.legend(loc='best')
    y_max = n_files * n_time * lat * long * 0.01
    plt.ylim([0, y_max])
    plt.xlabel('rain rate [mm/h]   (4-hourly mean)')
    plt.ylabel('p(rr)       (max: 0.01 * n_points)')

    plt.subplot(1, 3, 3)
    bin_max_ = 30
    width = 0.75 * (bin_arr[1] - bin_arr[0])
    center = (bin_arr[:bin_max_] + bin_arr[1:(bin_max_ + 1)]) / 2
    plt.bar(center, hist[:bin_max_], align='center', width=width)
    # percentiles:
    for i, ip in enumerate(per_arr[2, :]):
        ip = np.int(ip)
        if ip < bin_max_:
            plt.bar(center[ip], hist[ip], align='center', width=width,
                color=cm_r(np.double(i)/n_tot),
                label=np.str(per_arr[0, i]) + 'th percentile')
    plt.legend(loc='best')
    plt.ylim([0, hist[1] * 1.01])
    plt.xlabel('rain rate [mm/h]   (4-hourly mean)')
    plt.ylabel('p(rr)       (max: hist[1])')
    plt.title('(bin-width=0.1)')

    plt.suptitle('Histogram: 4-hourly rain rates ('
                 +np.str(date_list[0]) + '-' + np.str(date_list[-1]) + ')', fontsize=21)
    plt.savefig('./hist_all.png')
    plt.close()




    # Histogram wrt hist[1:]
    plt.figure(figsize=(27, 9))
    plt.subplot(1, 3, 1)
    width = 1. * (bin_arr[1] - bin_arr[0])
    center = (bin_arr[:-1] + bin_arr[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.title('(bin-width=0.1)')
    plt.ylim([0, hist[2] * 1.001])
    plt.xlabel('rain rate [mm/h]   (4-hourly mean)')
    plt.ylabel('p(rr)')

    plt.subplot(1, 3, 2)
    width = .75 * (bin_arr[1] - bin_arr[0])
    center = (bin_arr[:bin_max] + bin_arr[1:(bin_max + 1)]) / 2
    plt.bar(center, hist[:bin_max], align='center', width=width)
    plt.title('(bin-width=0.1)')
    # percentiles:
    for i, ip in enumerate(per_arr[3,:]):
        ip = np.int(ip)
        if ip < bin_max:
            plt.bar(center[ip], hist[ip], align='center', width=width,
                color=cm(np.double(i)/n_tot), hatch='//',
                label=np.str(per_arr[0,i])+'th percentile (i='+np.str(ip)+')')
    plt.legend(loc='best')
    y_max = n_files * n_time * lat * long * 0.01
    plt.ylim([0, y_max])
    plt.xlabel('rain rate [mm/h]   (4-hourly mean)')
    plt.ylabel('p(rr)       (max: 0.01 * n_points)')

    plt.subplot(1, 3, 3)
    bin_max = 30
    width = 0.75 * (bin_arr[1] - bin_arr[0])
    center = (bin_arr[:bin_max] + bin_arr[1:(bin_max + 1)]) / 2
    plt.bar(center, hist[:bin_max], align='center', width=width)
    # percentiles:
    for i, ip in enumerate(per_arr[3, :]):
        ip = np.int(ip)
        if ip < bin_max:
            plt.bar(center[ip], hist[ip], align='center', width=width,
                color=cm(np.double(i) / n_tot), hatch='//',
                label=np.str(per_arr[0, i]) + 'th percentile')
    plt.legend(loc='best')
    plt.ylim([0,hist[1]*1.01])
    plt.xlabel('rain rate [mm/h]   (4-hourly mean)')
    plt.ylabel('p(rr)       (max: hist[1])')
    plt.title('(bin-width=0.1)')

    plt.suptitle('Histogram: 4-hourly rain rates; Percentiles wrt Hist[1:] ('
                 + np.str(date_list[0]) + '-' + np.str(date_list[-1]) + ')', fontsize=21)
    plt.savefig('./hist_all_perc2.png')
    plt.close()

    return