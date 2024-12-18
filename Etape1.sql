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

--Phase 4.4 
--Création de la table snapshots 
CREATE TABLE snapshots (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    image BLOB,
    timestamp TIMESTAMP
);

--Récupérer le snapshots GET
SELECT id, TO_CHAR(timestamp, ''YYYY-MM-DD HH24:MI:SS'') AS ts,
                     UTL_RAW.CAST_TO_VARCHAR2(UTL_ENCODE.BASE64_ENCODE(image)) AS base64_image
                     FROM snapshots
--Procédure pour sauvergarder un Snapshots 
CREATE OR REPLACE FUNCTION BLOB_TO_BASE64(blob_data BLOB) RETURN CLOB IS
    base64_clob CLOB;
    raw_chunk RAW(2000); -- On utilise des chunks de taille plus petite pour éviter les dépassements
    chunk_size INTEGER := 2000; -- Taille du chunk ajustée
    blob_length INTEGER;
    offset INTEGER := 1; -- Début de lecture
BEGIN
    -- Créer un CLOB temporaire
    DBMS_LOB.CREATETEMPORARY(base64_clob, TRUE);

    -- Longueur totale du BLOB
    blob_length := DBMS_LOB.GETLENGTH(blob_data);

    -- Lire le BLOB en chunks et encoder en Base64
    WHILE offset <= blob_length LOOP
        -- Lire un chunk de données brutes
        raw_chunk := DBMS_LOB.SUBSTR(blob_data, chunk_size, offset);

        -- Encoder en Base64 et ajouter au CLOB
        DBMS_LOB.APPEND(base64_clob, UTL_RAW.CAST_TO_VARCHAR2(UTL_ENCODE.BASE64_ENCODE(raw_chunk)));

        -- Passer au prochain chunk
        offset := offset + chunk_size;
    END LOOP;

    RETURN base64_clob;
END;
/
CREATE OR REPLACE PROCEDURE SAVE_SNAPSHOT(image_base64 CLOB, ts VARCHAR2) IS
    decoded_image BLOB;
BEGIN
    -- Conversion explicite du timestamp reçu
    INSERT INTO snapshots (image, timestamp)
    VALUES (
        BASE64DECODECLOBTOTOBLOB(image_base64),
        TO_DATE(ts, 'YYYY-MM-DD HH24:MI:SS')
    );

    COMMIT;
END;
/


