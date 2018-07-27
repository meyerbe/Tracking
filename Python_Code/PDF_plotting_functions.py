import numpy as np
# import pylab as plt
import matplotlib
import matplotlib.pyplot as plt
import scipy
from scipy import stats

def plot_scatter_all(mean, variance, meanmean, varmean, extremes, dates):

    print('plotting')

    # Now switch to a more OO interface to exercise more features.
    # fig, axs = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(20,9))
    fig, axs = plt.subplots(nrows=1, ncols=2, sharex=False, figsize=(20,9))
    ax = axs[0] # ax = axs[0, 0]
    ax.plot(dates, mean, '.')
    for i in range(len(extremes)):
        ax.plot(extremes[i][2], extremes[i][1], '.r')
    ax.plot([dates[0],dates[-1]], [meanmean,meanmean], 'k--', linewidth=1, label='mean(means)')
    ax.plot([dates[0],dates[-1]], [meanmean+varmean,meanmean+varmean], 'k', linewidth=1, label=r'mean(means)$\pm$2*var(means)')
    ax.plot([dates[0],dates[-1]], [meanmean-varmean,meanmean-varmean], 'k', linewidth=1)
    ax.set_title('mean rain rates')
    ax.legend()
    plt.xlabel('dates')
    plt.ylabel('mean')

    ax = axs[1] #ax = axs[0, 1]
    ax.errorbar(dates, mean, yerr=variance, fmt='o')#, color='b')
    # ax.errorbar(extremes[:][2], extremes[:][1], yerr=variance, fmt='o', color='r')
    # ax.errorbar(extremes[:][2], extremes[:][1], fmt='o', color='r')
    for i in range(len(extremes)):
        ax.errorbar(extremes[i][2], extremes[i][1], fmt='o', color='r')
    ax.plot([dates[0], dates[-1]], [meanmean + varmean, meanmean + varmean], 'k', linewidth=1)
    ax.plot([dates[0], dates[-1]], [meanmean - varmean, meanmean - varmean], 'k', linewidth=1)
    ax.set_title('mean + var')
    plt.xlabel('dates')
    plt.ylabel('mean')
    plt.savefig('./alldata_mean_var.png')
    return



def plot_histogram_all(mean, variance, meanmean, varmean, extremes, date_list):

    import matplotlib.mlab as mlab

    print('plot histogram')


    plt.figure(figsize=(20,9))
    plt.subplot(1,2,1)
    # plt.hist(mean)
    num_bins = 20
    n, bins, patches = plt.hist(mean, num_bins, density=False, facecolor='green', alpha=0.5)
    plt.xlabel('mean')
    plt.ylabel('p(mean)')
    plt.title('all date, unnormed')

    plt.subplot(1,2,2)
    num_bins = 50
    n, bins, patches = plt.hist(mean, num_bins, density=True, facecolor='green', alpha=0.5)
    y = scipy.stats.norm.pdf(bins, meanmean, varmean)
    plt.plot(bins, y, 'r--', label='best fit normal distribution')
    plt.legend(loc='best')
    plt.xlabel('mean')
    plt.ylabel('p(mean)')
    plt.title('all date, normed')
    plt.savefig('./alldata_hist.png')

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