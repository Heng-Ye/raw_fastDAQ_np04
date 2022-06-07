#!/bin/bash

#raw_binary_path='/eos/experiment/neutplatform/protodune/np04tier0/ground_planes/'
#output_csv_path='/eos/user/h/heliao/protodune_hv/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0917_0919/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0917_0919/csv/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0914/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0914/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0913/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0913/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0915/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0915/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0907/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0907/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0910/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0910/'
#raw_binary_path='/media/hy/Seagate/GP_Data/gp_data_0919/'
#output_csv_path='/media/hy/Seagate/GP_Data/gp_data_0919/'
raw_binary_path='./data/'
output_csv_path='./data/'

COUNTER=0
for file in ${raw_binary_path}*.facq; do
#for file in ${raw_binary_path}*.facq.csv; do
  COUNTER=$((COUNTER+1))
  #echo 'evt:' $COUNTER

  #raw_binary_file=${raw_binary_path}${file##*/}
  raw_binary_file=${raw_binary_path}${file##*/}
  #output_csv_file=${raw_binary_path}${raw_binary_file}'.csv'
  output_csv_file=${raw_binary_file}'.csv'
  output_fig=${raw_binary_file}'_zoom.png'

  #binary to csv conversion
  echo '['$COUNTER']: ' $raw_binary_file
  #ls -ltr $raw_binary_file
  python decoder.py $raw_binary_file  $output_csv_file

  #evt display
  echo '  converted csv:' $output_csv_file
  #ls -ltr $output_csv_file
  python wf_display.py $output_csv_file $output_fig
  #python wf_display.py $raw_binary_file $output_fig

done
