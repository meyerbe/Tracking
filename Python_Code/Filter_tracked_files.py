import os
import glob
import ntpath
import numpy as np
import netCDF4 as nc


# Select days based on:
#       - large (enough) number of deep convective events (area and rain intensity)
#       - small advection

# Output data:
# (a)   advection velocit in: irt_advection_field_19981206.srv (SERVICE-file >> converted to nc-file)
# (b)	Area: irt_objects_output.txt >> 4th column (Text-file)
# (c)	Intensity: irt_objects_output.txt >> 5th column (Mean value of the tracker field, averaged over the object's area) (Text-file)

# The SERVICE-files (e.g., masks) can be converted to NetCDF e.g. by the CDO command cdo -f nc copy irt objects mask.srv irt objects mask.nc
# >> cdo -f nc copy irt tracks mask.srv irt tracks mask.nc


def main():
    path_data = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data'


    ''' (a) Advection Velocity '''
    # Data structure:
    # Variables:
    # - time: units = "day as %Y%m%d.%f";
    # - lev: axis = "Z"; (vertical level)
    # - var1(time, lev, y, x); var2(time, lev, y, x); var3(time, lev, y, x);

    # (i) read in netcdf-file
    files_vel = [name for name in os.listdir(path_data) if name[4:13] == 'advection']
    n_files_vel = len(files_vel)
    print('# files vel: ' + np.str(n_files_vel))
    print('')

    # path_in = os.path.join(path_data, files_vel[0])
    # rootgrp = nc.Dataset(path_in, 'r')
    # var = rootgrp.variables['radar_estimated_rain_rate']
    # rootgrp.close()

    for path_in in glob.glob(os.path.join(path_data, '*.nc')):
        data_name = ntpath.basename(path_in)[:-4]
        date = data_name[-8:]
        print('name: ', data_name)
        print(path_in)

        rootgrp = nc.Dataset(path_in, 'r')
        var = rootgrp.variables['var1']
        vel_adv = np.ndarray(shape=(np.append(3,var.shape)))
        vel_adv[0,:] = var[:]
        var = rootgrp.variables['var2']
        vel_adv[1,:] = var[:]
        var = rootgrp.variables['var3']
        vel_adv[2,:] = var[:]


        rootgrp.close()
        print('vel adv: ', vel_adv.shape)



    return



# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()

