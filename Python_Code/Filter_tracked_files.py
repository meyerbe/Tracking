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



    path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data'
    # path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data_test'

    # path_in = os.path.join(path_data, files_vel[0])
    # rootgrp = nc.Dataset(path_in, 'r')
    # var = rootgrp.variables['radar_estimated_rain_rate']
    # rootgrp.close()

    ''' (a) Advection Velocity '''
    # Data structure:
    # Variables:
    # - time: units = "day as %Y%m%d.%f"    (time = 6)
    # - lev: axis = "Z"; (vertical level)   (lev = 1)
    # - x, y: division of domain for advection vel computation in tracking algorithm
    #                                       (x = y = 2)
    # - var1(time, lev, y, x); var2(time, lev, y, x); var3(time, lev, y, x);
    #       >> dim(var1) = time * lev * y * x = 6 * 1 * 2 * 2
    #       >> var1 = (time, lev, y, x) = (6, 1, 2, 2)

    # (i) read in netcdf-file
    if flag_adv_vel:
        files_vel = [name for name in os.listdir(path_data) if name[4:13] == 'advection']
        n_files_vel = len(files_vel)
        print('# files vel: ' + np.str(n_files_vel))        # all files: 5250
        print('')
        # read in test file
        path_in = os.path.join(path_data, 'irt_advection_field_20011031.nc')
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


    count = 0
    for path_in in glob.glob(os.path.join(path_data, '*.nc')):
        data_name = ntpath.basename(path_in)[:-4]
        date = data_name[-8:]
        print('name: ', data_name)
        print(path_in)

        if flag_adv_vel:
            if data_name[4:13] == 'advection':
                rootgrp = nc.Dataset(path_in, 'r')
                var = rootgrp.variables['var1']
                vel_adv = np.ndarray(shape=(np.append(3,var.shape)))
                vel_adv[0,:] = var[:]
                var = rootgrp.variables['var2']
                vel_adv[1,:] = var[:]
                var = rootgrp.variables['var3']
                vel_adv[2,:] = var[:]
                rootgrp.close()

                vel_norm = np.linalg.norm(vel_adv, axis=0)      # vel_norm = (6, 1, 2, 2)

                vel_norm_coll = np.append(vel_norm_coll, np.ravel(vel_norm))
                vel_norm_domain_coll = np.append(vel_norm_domain_coll, np.mean(np.mean(vel_norm[:,:,:,:], axis=3), axis=2))
                vel_norm_domain_daily_coll = np.append(vel_norm_domain_daily_coll,np.mean(vel_norm))

                print('vel norm: ', vel_norm.shape, vel_adv.shape, np.ravel(vel_norm).shape, 6*1*2*2)
                print('vel norm coll: ', type(vel_norm_coll), np.shape(vel_norm_coll))

        count += 1
    # print('total: ', np.sum(vel_norm_domain_daily_coll))


    if flag_adv_vel:
        plot_adv_vel_hist(vel_norm_coll, vel_norm_domain_coll, vel_norm_domain_daily_coll, path_data)




    return

# ----------------------------------------------------------------------

def plot_adv_vel_hist(vel_norm_coll, vel_norm_domain, vel_norm_domain_daily_coll, path_data):
    # plot histogram of advection velocity norm

    bin_width = 1.
    bin_arr = np.arange(0, 51, bin_width)
    # print('arr', bin_arr)
    plt.figure(figsize=(19, 6))
    plt.subplot(1,3,1)
    plt.hist(vel_norm_coll, bins=bin_arr, rwidth=0.75)
    plt.xlabel('norm(vel)', fontsize=15)
    plt.ylabel('p[norm(vel)]', fontsize=15)
    plt.title('4-hourly advection per sector (bins='+str(bin_width)+')')

    plt.subplot(1, 3, 2)
    bin_width = 1.
    bin_arr = np.arange(0, 31, bin_width)
    plt.hist(vel_norm_domain, bins=bin_arr, rwidth=0.75)
    plt.xlabel('norm(<vel>)', fontsize=15)
    plt.ylabel('p[norm(<vel>)]', fontsize=15)
    plt.title('4-hourly domain mean advection (bins='+str(bin_width)+')')

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

