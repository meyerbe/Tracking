import os
import glob
import ntpath
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt


# Select days based on:
#       - large (enough) number of deep convective events (area and rain intensity)
#       - small advection

# Output data:
# (a)   advection velocity in: irt_advection_field_19981206.srv (SERVICE-file >> converted to nc-file)
# (b)	Area: irt_objects_output.txt >> 4th column (Text-file)
# (c)	Intensity: irt_objects_output.txt >> 5th column (Mean value of the tracker field, averaged over the object's area) (Text-file)

# The SERVICE-files (e.g., masks) can be converted to NetCDF e.g. by the CDO command cdo -f nc copy irt objects mask.srv irt objects mask.nc
# >> cdo -f nc copy irt tracks mask.srv irt tracks mask.nc


def main():
    flag_adv_vel = True         # read in advection velocity



    # path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data'
    path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data_test'

    # path_in = os.path.join(path_data, files_vel[0])
    # rootgrp = nc.Dataset(path_in, 'r')
    # var = rootgrp.variables['radar_estimated_rain_rate']
    # rootgrp.close()

    ''' (a) Advection Velocity Histogram'''
    # Data structure:
    # Variables:
    # - time: units = "day as %Y%m%d.%f"    (time = 6)
    # - lev: axis = "Z"; (vertical level)   (lev = 1)
    # - x, y: division of domain for advection vel computation in tracking algorithm
    #                                       (x = y = 2)
    # - var1(time, lev, y, x); var2(time, lev, y, x); var3(time, lev, y, x);
    #       >> dim(var1) = time * lev * y * x = 6 * 1 * 2 * 2
    #       >> var1 = (time, lev, y, x) = (6, 1, 2, 2)
    #
    # Generated Data:
    # dict_vel_norm_domain[date]:           dictionary >> contains for each date a (6,1)-array for the domain averaged velocity norm in 4-hourly intervals
    #

    date_arr = []           # array with all data


    # (i) read in netcdf-file
    if flag_adv_vel:
        files_vel = [name for name in os.listdir(path_data) if (name[4:13] == 'advection' and name[-3:] == '.nc')]
        # files_vel = [name for name in os.listdir(path_data) if (name[4:24] == 'advection_field_it1_' and name[-3:] == '.nc')]
        n_files_vel = len(files_vel)
        print('# files vel: ' + np.str(n_files_vel))        # all files: 5250
        print(files_vel)
        print('')
        # read in test file
        path_in = os.path.join(path_data, files_vel[0])
        rootgrp = nc.Dataset(path_in, 'r')
        vel_x = rootgrp.variables['var1']
        n_time = vel_x.shape[0]
        n_lev = vel_x.shape[1]
        n_y = vel_x.shape[2]
        n_x = vel_x.shape[3]

        # for histogram
        vel_norm_coll = []
        vel_norm_domain_coll = []
        vel_norm_domain_daily_coll = []

        dict_vel_norm_domain = {}
        dict_vel_norm_domain_day = {}
        # print('dict:', type(dict_vel_norm_domain), dict_vel_norm_domain)

    # ''' (A) Collect data (general)'''
    # for path_in in glob.glob(os.path.join(path_data, '*.nc')):
    #     data_name = ntpath.basename(path_in)[:-3]
    #     date = data_name[-8:]
    #     ''' (i) read in advection velocity components & compute norm '''
    #     if data_name[4:13] == 'advection':
    #         pass


    # ''' (A) Test if velocity data different for all days'''
    # test_vel_data(files_vel, path_data, n_time, n_x, n_y)


    ''' (B) Collect velocity data '''
    if flag_adv_vel:
        for data_name in files_vel:

            ''' (i) read in advection velocity components & compute norm '''
            path_in = os.path.join(path_data, data_name)
            rootgrp = nc.Dataset(path_in, 'r')
            print('file: ', data_name, path_in)
            var = rootgrp.variables['var1']

            if var.shape[0] < 12:
                print('PROBLEM WITH VAR SHAPE: ' + str(var.shape))
                print('')
                continue
            print('var:      ', var.shape)

            vel_adv = np.ndarray(shape=(np.append(3,var.shape)))
            vel_adv[0,:] = var[:]
            var = rootgrp.variables['var2']
            vel_adv[1,:] = var[:]
            var = rootgrp.variables['var3']
            vel_adv[2,:] = var[:]
            rootgrp.close()

            ''' (ii) compute velocity norms '''
            vel_norm = np.linalg.norm(vel_adv, axis=0)      # vel_norm = (6, 1, 2, 2)

            # collect for all data >> histogram
            vel_norm_coll = np.append(vel_norm_coll, np.ravel(vel_norm))
            # average over domain & collect for all data >> histogram
            vel_norm_domain_coll = np.append(vel_norm_domain_coll, np.mean(np.mean(vel_norm[:,:,:,:], axis=3), axis=2))
            # average over domain and day & collect for all data >> histogram
            vel_norm_domain_daily_coll = np.append(vel_norm_domain_daily_coll,np.mean(vel_norm))

            ''' (iii) save all dates with complete data in array '''
            date = data_name[-11:-3]
            date_arr = np.append(date_arr, date)

            # dictionary: contains for each date a (12,1)-array for the domain averaged velocity norm in 4-hourly intervals
            dict_vel_norm_domain[date] = np.mean(np.mean(vel_norm[:,:,:,:], axis=3), axis=2)
            dict_vel_norm_domain_day[date] = np.mean(vel_norm)

            print('')

    print('')
    print('vel norm:                   ', vel_norm.shape)
    print('vel norm coll:              ', vel_norm_coll.shape)
    print('vel norm domain coll:       ', vel_norm_domain_coll.shape)
    print('vel norm domain daily coll: ', vel_norm_domain_daily_coll.shape)
    print('')
    d = date_arr[0]
    print('dict vel norm domain:       len: ', len(dict_vel_norm_domain),     'element shape: ', dict_vel_norm_domain[d].shape)
    print('dict vel norm daily domain: len: ', len(dict_vel_norm_domain_day), 'element shape: ', dict_vel_norm_domain_day[d].shape)
    print('')


    # ''' (B) plotting '''
    # if flag_adv_vel:
    #     ''' (i) plot velocity histogram '''
    #     plot_adv_vel_hist(vel_norm_coll, vel_norm_domain_coll, vel_norm_domain_daily_coll, n_time, path_data)




    ''' (C) filtering'''
    print('')
    print('dates: ', date_arr)
    print('')
    # print(dict_vel_norm_domain)
    # print('')
    # print(dict_vel_norm_domain_day)
    # print('')

    max_v_norm = 5.             # threshold for 2-hourly mean advection velocity
    max_v_norm_daily = 2.5       # threshold for daily mean advection velocity
    dict_adv_small = {}
    dict_adv_small_daily = {}
    if flag_adv_vel:
        for d in date_arr:
            print('date', d)

            if dict_vel_norm_domain_day[d] > max_v_norm_daily:
                print('big (daily): ' + np.str(dict_vel_norm_domain_day[d]) )
            else:
                print('small (daily): ' + np.str(dict_vel_norm_domain_day[d]) )
                dict_adv_small_daily[d] = dict_vel_norm_domain_day[d]

            if np.any(dict_vel_norm_domain[d] > max_v_norm):
                print('big')
            else:
                print('small')
                dict_adv_small[d] = dict_vel_norm_domain[d]
        print('')
        print('small advection: ', dict_adv_small)
        print('')
        print('small advection daily: ', dict_adv_small_daily)







    return

# ----------------------------------------------------------------------
''' Test if velocity data different for all days'''
def test_vel_data(files_vel, path_data, n_time, n_x, n_y):
    plt.figure()
    for data_name in files_vel:
        ''' read in advection velocity components & compute norm '''
        path_in = os.path.join(path_data, data_name)
        rootgrp = nc.Dataset(path_in, 'r')
        var = rootgrp.variables['var1']

        if var.shape[0] < 12:
            print('PROBLEM WITH VAR SHAPE: ' + str(var.shape))
            print('file: ', data_name, path_in)
            continue

        vel_adv = np.ndarray(shape=(np.append(3, var.shape)))
        vel_adv[0, :] = var[:]
        var = rootgrp.variables['var2']
        vel_adv[1, :] = var[:]
        var = rootgrp.variables['var3']
        vel_adv[2, :] = var[:]
        rootgrp.close()

        for i in range(n_time):
            for y_ in range(n_y):
                for x_ in range(n_x):
                    plt.plot([0, vel_adv[0, i, :, y_, x_]], [0, vel_adv[1, i, :, y_, x_]],
                             '-o')  # , label='i, date='+np.str(date))

    # plt.legend()
    plt.xlabel('v_x')
    plt.ylabel('v_y')
    d_min = files_vel[0][-11:-3]
    d_max = files_vel[-1][-11:-3]
    plt.title('v_x vs. v_y')
    plt.title('v_x vs. v_y ('+str(d_min)+'-'+str(d_max)+')')
    plt.savefig(os.path.join(path_data, 'adv_vel_vectorfig.png'))

    return
# ----------------------------------------------------------------------

def plot_adv_vel_hist(vel_norm_coll, vel_norm_domain, vel_norm_domain_daily_coll, n_time, path_data):
    # plot histogram of advection velocity norm

    bin_width = 1.
    bin_arr = np.arange(0, 51, bin_width)
    # print('arr', bin_arr)
    plt.figure(figsize=(19, 6))
    plt.subplot(1,3,1)
    plt.hist(vel_norm_coll, bins=bin_arr, rwidth=0.75)
    plt.xlabel('norm(vel)', fontsize=15)
    plt.ylabel('p[norm(vel)]', fontsize=15)
    plt.title(str(np.int(24/n_time))+'-hourly advection per sector (bins='+str(bin_width)+')')

    plt.subplot(1, 3, 2)
    bin_width = 1.
    bin_arr = np.arange(0, 31, bin_width)
    plt.hist(vel_norm_domain, bins=bin_arr, rwidth=0.75)
    plt.xlabel('norm(<vel>)', fontsize=15)
    plt.ylabel('p[norm(<vel>)]', fontsize=15)
    plt.title(str(np.int(24/n_time))+'-hourly domain mean advection (bins='+str(bin_width)+')')

    plt.subplot(1, 3, 3)
    bin_width = 0.1
    bin_arr = np.arange(0, 6, bin_width)
    plt.hist(vel_norm_domain_daily_coll, bins=bin_arr, rwidth=0.75)
    plt.xlabel('norm(<vel>)', fontsize=15)
    plt.ylabel('p[norm(<vel>)]', fontsize=15)
    plt.title('daily domain mean advection (bins='+str(bin_width)+')')

    plt.suptitle('Histogram: norm advection velocities (bin width = ' + str(bin_width) + ')', fontsize=21)
    plt.savefig(os.path.join(path_data, 'adv_vel_norm_hist.png'))
    return

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()

