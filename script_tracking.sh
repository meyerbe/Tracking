#!bin/bash/

echo "running tracking script"

# Input path to data
#read -p "Path to DARWIN data:" path_darwin
#path_darwin=/Users/bettinameyer/polybox/ClimatePhysics/Copenhagen/Projects/RadarData_Darwin/RADAR_ESTIMATED_RAIN_RATE
path_darwin=/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/RADAR_ESTIMATED_RAIN_RATE
echo "Data files in $path_darwin"

# Path to copy output to
#path_out=/Users/bettinameyer/polybox/ClimatePhysics/Copenhagen/Projects/RadarData_Darwin/Radar_Tracking_Data
path_out=/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data
path_irt=iterative_raincell_tracking_laptop

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


# ---------------------------------------------------------------------------------------
#             LOOP OVER FILES
# ---------------------------------------------------------------------------------------

##if [ year_min=" " ]
##  then year_min=2002
##fi

# Loop over all files in repository
#for year in {$year_min..$year_max}
#for year in {1998..2017}
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
  
      name="CPOL_RADAR_ESTIMATED_RAIN_RATE_${date}.nc"
      echo $name
      # --- check if file there ---
      if [ -f $path_darwin/$name ]
        then
        echo "The file ${name} exists."
        else
        echo "!!! The file ${name} does not exist."
        continue                                          # go to next file name in for loop
      fi

      # --- convert file into service-file (file automatically copied into working repository) ---
      # DARWIN Radar files only have one variable: radar_estimated_rain_rate
      echo "(1) convert data into *.srv-file"
      cdo -f srv selvar,radar_estimated_rain_rate $path_darwin/$name $path_irt/irt_objects_input_00.srv

      cd iterative_raincell_tracking_laptop
      echo $PWD

      # Run tracking: 1st iteration
      echo "(2) run 1st iteration"
      # --- (a1) object identification ---
      ./irt_objects_v1.x 1
      #cp irt_objects_output.txt $path_out/irt_objects_output_${date}.txt
      #cp irt_objects_mask.srv $path_out/irt_objects_mask_${date}.srv
      # --- (b1) advection velocity ---
      ./irt_advection_field_v1.x
      #cp irt_advection_field.srv $path_out/irt_advection_field_${date}.srv
      # --- (c1) track identification ---
      ./irt_tracks_v1.x
      #cp irt_tracks_output.txt $path_out/irt_tracks_output_${date}.txt
      # --- (d1) generate object mask file (*.srv) ---
      sort -n -k2 irt_tracks_nohead_output.txt > irt_tracks_sorted.txt
      ./irt_trackmask_v1.x
      #cp irt_tracks_mask.srv $path_out/irt_tracks_mask_${date}.srv

      echo "(3) run 2nd iteration"
      # --- (a2) ---
      ./irt_objects_v1.x 2
      # --- (b2) advection velocity ---
      ./irt_advection_field_v1.x
      cp irt_advection_field.srv $path_out/irt_advection_field_${date}.srv
      cdo -f nc copy irt_advection_field.srv irt_advection_field.nc
      cp irt_advection_field.nc $path_out/irt_advection_field_${date}.nc 
      # --- (c2) track identification ---
      ./irt_tracks_v1.x
      cp irt_tracks_output.txt $path_out/irt_tracks_output_${date}.txt
      # --- (d2) generate object mask file (*.srv) ---
      sort -n -k2 irt_tracks_nohead_output.txt > irt_tracks_sorted.txt
      ./irt_trackmask_v1.x
      cp irt_tracks_mask.srv $path_out/irt_tracks_mask_${date}.srv

    done
  done  
done


