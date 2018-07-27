#!bin/bash/

echo "converting srv-advection file to nc-file"

# path where data are stored
#path_data=/Users/bettinameyer/polybox/ClimatePhysics/Copenhagen/Projects/RadarData_Darwin/Radar_Tracking_Data
path_data=/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data

# year min: 1998; year max: 2017
# months: 01, 02, 03, 04, 10, 11, 12
read -p "year min: " year_min; read -p "year max: " year_max
read -p "month min: " month_min; read -p "month max: " month_max
read -p "day min: " day_min; read -p "day max: " day_max

# if no input for year_min, run single day
if [[ ! -z $year_min ]]
  then
  do_flag="loop"
else
  do_flag="single"
fi

case $do_flag in
  "loop")
  echo "running loop"
  ;; # finishing 'loop'-case

  "single")
  year_min=2002
  year_max=2002
  month_min=1
  month_max=1
  day_min=1
  day_max=1
  echo "running single day: $day_min.$month_min.$year_min"
  ;; # finishing 'single'-case

esac



# --- filenames to convert ---
file_name_vel="irt_advection_field"

# ---------------------------------------------------------------------------------------
#             LOOP OVER FILES
# ---------------------------------------------------------------------------------------

for (( year=$year_min; year<=$year_max; year++ ))
  do
  echo "year: $year"
  #for month in {1..12}
  for (( month=$month_min; month<=$month_max; month++ ))
    do
    #echo "month: $month"
    #for day in {1..31}
    for (( day=$day_min; day<=day_max; day++ ))
      do
      #echo $day

      date=$(($year*10000+$month*100+$day))
      echo "Date: $date"

      # ---convert velocity file into netcdf-file ---
      # --- check if file there ---
      if [ -f $path_data/irt_advection_field_${date}.srv ]
        then
        echo "The file irt_advection_field_${date}.srv exists."
        else
        echo "!!! The file irt_advection_field_${date}.srv does not exist."
        continue                                          # go to next file name in for loop
      fi
      cdo -f nc copy $path_data/irt_advection_field_${date}.srv $path_data/irt_advection_field_${date}.nc


    done
  done
done
