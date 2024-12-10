CREATE OR REPLACE DIRECTORY data_dir AS '/u01/app';

SELECT directory_name, directory_path
FROM all_directories
WHERE directory_name = 'DATA_DIR';

CREATE TABLE projet_overview (
    DeviceTimeStamp CHAR(20),
    OTI NUMBER,
    WTI NUMBER,
    ATI NUMBER,
    OLI NUMBER,
    OTI_A NUMBER,
    OTI_T NUMBER,
    MOG_A NUMBER
)
ORGANIZATION EXTERNAL
(
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY data_dir
    ACCESS PARAMETERS
    (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
        MISSING FIELD VALUES ARE NULL
        (DeviceTimeStamp CHAR(20),
         OTI FLOAT,
         WTI FLOAT,
         ATI FLOAT,
         OLI FLOAT,
         OTI_A FLOAT,
         OTI_T FLOAT,
         MOG_A FLOAT)
    )
    LOCATION ('Overview.csv')
)
REJECT LIMIT UNLIMITED;