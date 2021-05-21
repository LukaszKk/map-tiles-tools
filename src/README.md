# Description
An application that converts raster data to XYZ format.
Requires data from British map agency in scale 1:250000 or 1:50000 put in a directory ./input/data/<250k or 50k>.
In case of using parallelism requires putting in a directory ./input/data/groups/<3 or 3-250 or 7 or 7-250> files with names group<x>.csv containing 2 columns (fileName,filePath) with a name and path to input files included in specified group. 

## Additional Requirements
    Gdal 3.1+
    
## Parameters
    k : generate output of input data 50k. If not defined generates output of input data 250k
    z <level> : generate output data for defined <level>
    m <method> : use one of below methods as a simultaneous way of generation
        s, single : generate data without parallel mode. Parameter -g is ignored.
        mt, multithreading : use multiple threads in parallel mode 
        mp, multiprocessing : use multiple processes in parallel mode 
        r, ray : use ray library in parallel mode
    g <groups> : define number of groups to generate simultaneously
    
## Example of execution
### 50k
    python src\\Main.py -k -z 13 -m single -g 3
### 250K
    python src\\Main.py -z 11 -m mp -g 7
