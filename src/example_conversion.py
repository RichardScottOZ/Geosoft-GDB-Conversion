import os
import numpy as np
import pandas as pd
import xarray as xr
# Initialize the gx environment
import geosoft.gxpy.gdb as gxdb
import geosoft.gxpy.gx as gxp

file_name = 'banana_splits.gdb'
output_dir = 'sour_grapes_bunch'

try:
    with gxp.GXpy() as gxp:
        # Open the Geosoft database
        # Database of lines with channels for each line and an array often (N, 2) for each channel
        gdb = gxdb.Geosoft_gdb.open(file_name)
        channels = list(gdb.list_channels().keys())

        data_dict = {}
        count = 0
        
        for line in gdb.list_lines():
            print("FL:",file_name,line,flush=True)
            count += 1
            data_dict[line] = {}
            
            for channel in channels:
                #print("FLC:",file_name,line,channel,flush=True)
                mag_data = gdb.read_channel_vv(line, channel)
                np_data = np.asarray(mag_data)
                data_dict[line][channel] = np.asarray(np_data)
    
    datasets = {}

    for line in data_dict:
        datasets[line] = xr.Dataset()
        for channel in data_dict[line]:
            data = data_dict[line][channel][:,0]
            fiducial = np.arange(len(data))  # Create a fiducial coordinate
            datasets[line][channel] = xr.DataArray(data, dims=['fiducial'], coords={'fiducial': fiducial})
    
            datasets[line][channel] = datasets[line][channel].expand_dims(dim='line')
    
            # Assign the line number as a coordinate
            datasets[line][channel] = datasets[line][channel].assign_coords(line=[line])
        
    print("FILENAME DATASETS:", file_name,datasets,flush=True)
    
    linelist= []
    for line in datasets:
        linelist.append(datasets[line])
        nested_datasets = linelist
    
    # Combine the nested datasets along specified dimensions
    combined_dataset = xr.combine_nested(nested_datasets, concat_dim=['line'])
    
    print("FILENAME COMBINED:", file_name,combined_dataset,flush=True)
    # Stack the 'line' and 'fiducial' dimensions into a single 'stacked_line_fiducial' dimension
    # netcdf / zarr don't like the nesting in the above, so this simplies
    try:
        combined_dataset = combined_dataset.reset_index(['fiducial', 'line'], drop=True)
    except Exception as noresetE:
        pass
    
    #Now save the dataset
    print("WRITING ZARR!:", file_name)
    try:
        combined_dataset.to_zarr(output_dir + "\\" + file_name + '.zarr',mode='w')
    except Exception as nozarrE:
        combined_dataset.to_netcdf(output_dir + "\\" + file_name + '.nc')

    print("FILENAME ZARR DONE!:", file_name)
except Exception as nogoodE:
    print("ERROR:", file_name, nogoodE)
