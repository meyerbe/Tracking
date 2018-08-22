import os
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser(prog='PyCLES')
    parser.add_argument("--threshold")
    args = parser.parse_args()

    if args.threshold:
        threshold = np.int(args.threshold)
    else:
        threshold = 100

    path = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data/1_irt_objects_output'
    date = 19981207
    file_name = 'irt_objects_output_' + str(date) + '.txt'
    # print(file_name)

    path_track = '/Users/bettinameyer/Dropbox/ClimatePhysics/Code/Tracking/RadarData_Darwin/Radar_Tracking_Data/2_irt_tracks_output'
    date = 19981207
    file_name_track = 'irt_tracks_output_' + str(date) + '.txt'


    # # f = open(os.path.join(path, file_name), 'r')
    f = open(os.path.join(path_track, file_name_track), 'r')
    #
    # # # read entire file
    # # print f.read()
    # # print('')
    # #
    # # read the first five characters of stored data and return it as a string:
    # print f.read(100)
    #
    # # read file line by line
    # print f.readline()
    #
    # # return n-th line of file
    # # print f.readline(5)
    # # print('')
    # # print('')
    # # print f.readline(-1)
    # # print('')
    # # print('')
    # #
    # # # print f.readlines(1)
    # #
    # #
    # data = f.readlines()
    # for line in data:
    #     words = line.split()
    #     print words
    #     print('')
    #
    f.close()




    find_days_with_large_number_of_cells()

    return



def find_days_with_large_number_of_cells(path_track, threshold):
    # SHOWS ALL DATES WHERE THE NUMBER OF PRECIPITATING CELLS IS LARGER THAN THE GIVEN THRESHOLD VALUE

    max_n_tracks = -9999
    min_n_tracks = 9999
    sum_n_tracks = 0
    count = 0

    files = [name for name in os.listdir(path_track) if name[-3:] == 'txt']
    n_files = len(files)
    # access last line of file
    for file_name_track in files:
        date = file_name_track[-12:-4]
        path = os.path.join(path_track, file_name_track)
        # print path
        with open(path, 'r') as f:
            lines = f.read().splitlines()
            if len(lines)>=1:
                last_line = lines[-1]
                words = last_line.split()
                s = np.int(words[0])
                if s > max_n_tracks:
                    max_n_tracks = s
                if s < min_n_tracks:
                    min_n_tracks = s
                sum_n_tracks += s
                if s > threshold:
                    print(date)
                    count += 1
    print('max # tracks: ', max_n_tracks)
    print('min # tracks: ', min_n_tracks)
    print('average # tracks: ', sum_n_tracks/n_files)
    print('# tracks > ' + str(threshold) +': ', count, '(total # files: '+str(n_files)+')')
    return

if __name__ == '__main__':
    main()