# Pre-processing pipeling

The pre-processing pipeline generates a processed .CSV file for data from wearable devices.

Currently, the pipeline is capable of pre-processing raw data from the following watches:
1. Apple Watch
2. Fitbit Watch
3. Garmin Watch
4. Miband
5. ECG data stored as a EDF file
6. Biovotion
7. Empatica


### Steps to use the pipeline

The pipeline requires the pandas, numpy, pytz, datetime, os, sys, json, rowingdata, mne, and re packages.

```
$ git clone https://github.com/DigitalBiomarkerDiscoveryPipeline/Pre-process.git
In your local machine go to :
$ cd /Pre-process/pipeline
Run `Complete - Browse file` file or 'Complete - User path`

```
#### If using the `Complete - Browse file` version of the code
1. The pipeline provides an option to browse the raw file in case of `Apple`, `Fitbit`, `Garmin`, `miband` and `ECG`. Please make sure to use these keywords when prompted to enter the `Type of watch`.

2. For `biovotion` and `empatica`, please provide the path to the folder where all the raw files are stored.

3. In case of `biovotion`, you will be prompted to enter the Device ID, you can find the same in the file name right after the vital sign name.
   For instance : If the filename is bop_1566404978515_BHR_5cda2e5e70116a01001eb098_1563897600_1563903059.csv, the Device ID is 5cda2e5e70116a01001eb098
   
4. The processed .csv file will be stored in the current working directory.

#### If using the `Complete - User path` version of the code
1. Please provide the path to the file / folder for the watch selected.

2. For `biovotion` and `empatica`, please provide the path to the folder where all the raw files are stored.

3. In case of `biovotion`, you will be prompted to enter the Device ID, you can find the same in the file name right after the vital sign name.
   For instance : If the filename is bop_1566404978515_BHR_5cda2e5e70116a01001eb098_1563897600_1563903059.csv, the Device ID is 5cda2e5e70116a01001eb098
   
4. The processed .csv file will be stored in the current working directory.

### Functions

The pipeline currently uses the following functions.

| Plugin | README |
| ------ | ------ |
| preprocessed_output | main function that calls respective functions based on choice of watch|
| readcsv | calls pandas read_csv function with or without header |
| apple | function to process raw data from apple watch |
| fitbit | function to process raw data from fitbit watch |
| garmin | function to process raw data from garmin watch |
| miband | function to process raw data from miband watch |
| ecg | function to process raw ecg data stored as a .EDF file |
| biovotion | function to process raw data from biovotion watch |
| empatica | function to process raw data from empatica watch |
| process_df | Modifies column names and adds watch types |
| output | Stores output file with watch name  |
| get_filenames | Used by biovotion and empatica to obtain all .csv files in a folder  |
| preprocess_empatica | Pre-processing function for empatica, used to obtain values of vitals and frequency rate |
| add_time_empatica | Add time function for empatica, used to add time for each vital sign |

##### apple functions:
    main : calls all other functions to process raw data
    dict_df : Creates a data dictionary with information like Workout_date, Duration, Calories burnt, Mean heart rate, Maximum heart rate, and Notes
    pre_process_apple : Creates a header for the apple dataframe
    add_time : Calculates actual time using start time and elapsed time information
    rename_cols : Renames column names of the dataframe
    output_dict : Outputs apple watch processed data as .csv and data dictionary as a .json file
##### fitbit functions:
    main : calls all other functions to process raw data
    add_time : Calculates elapsed time using actual time information
    rename_cols : Renames column names of the dataframe
##### garmin functions:
    main : calls all other functions to process raw data
    add_time : Obtains actual time by converting timestamp to UTC. Also calculates elapsed time using actual time information
    rename_cols : Renames column names of the dataframe

##### miband functions:
    main : calls all other functions to process raw data
    add_time : Calculates elapsed time using actual time information
    rename_cols : Renames column names of the dataframe

##### ecg functions:
    get_data : Processes .EDF file to obtain raw data in a .CSV file. It stores raw data as a .CSV file in the current working directory. 
    main : calls all other functions to process raw data
    pre_process_ECG : Drop unnecessary data columns from raw data .CSV file
    add_time : Calculates elapsed and actual time using start time and sampling rate information
    rename_cols : Renames column names of the dataframe

##### biovotion functions:
    main : calls all other functions to process raw data
    extract_names : Extracts names of the vital signs being measured by the watch using .CSV filenames
    read_data : Reads all CSV files in the folder containing vital sign measurements. Processes column names.
    create_df_final : Creates one single dataframe
    add_time : Calculates actual time by converting timestamp to UTC time. Also calculates elapsed time.

##### empatica functions:
    read_data : Reads all .CSV files data stored in the folder and processes each file. It calculates time using sampling frequency and start time for each file.
    all_dfs : All dataframes are combined to create one single dataframe
    main : calls all other functions to process raw data

### Continued Development

We are frequently updating this package with new devices and insights from the DBDP (Digital Biomarker Discovery Pipeline).
