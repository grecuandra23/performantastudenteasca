LIBNAME proiect '/home/u64505510/Proiect';

PROC FORMAT;
    VALUE $yesno_fmt  
        'yes' = 'Da'
        'no'  = 'Nu';
RUN;

DATA proiect.studenti2;
    SET proiect.studenti;

    IF MISSING(Nota_T1)     THEN Nota_T1 = 0;
    IF MISSING(Nota_T2)     THEN Nota_T2 = 0;
    IF MISSING(Nota_Finala) THEN Nota_Finala = 0;

    length Suport_Educational $ 15
           Risc_Abandon $ 13
           Eligibil_Bursa $ 11;

    IF Ajutor_Familie = 'yes' AND 
       Meditatii_Private = 'yes' AND 
       Meditatii_Scoala = 'yes' AND
       Internet = 'yes' THEN 
            Suport_Educational = 'Suport complet';
    ELSE IF Ajutor_Familie = 'yes' OR 
            Meditatii_Private = 'yes' OR 
            Meditatii_Scoala = 'yes' OR
            Internet = 'yes' THEN 
            Suport_Educational = 'Suport partial';
    ELSE Suport_Educational = 'Fara suport';

    NrRisc = 0;
    IF Suport_Educational = 'Fara suport' THEN NrRisc + 1;
    IF Absente > 8                         THEN NrRisc + 1;
    IF Materii_Picate >= 2                 THEN NrRisc + 1;
    IF Ore_Studiu <= 2                     THEN NrRisc + 1;

    IF NrRisc >= 3      THEN Risc_Abandon = 'Risc ridicat';
    ELSE IF NrRisc = 2  THEN Risc_Abandon = 'Risc mediu';
    ELSE                     Risc_Abandon = 'Risc scazut';

    
    
    
    Medie_Note = ROUND(MEAN(Nota_T1, Nota_T2, Nota_Finala), 0.01);

    IF Nota_Finala > 5 THEN Eligibil_Bursa = 'Eligibil';
    ELSE Eligibil_Bursa = 'Neeligibil';

    IF Suport_Educational = 'Suport complet' THEN OrdineSuport = 1;
    ELSE IF Suport_Educational = 'Suport partial' THEN OrdineSuport = 2;
    ELSE OrdineSuport = 3;

    IF Risc_Abandon = 'Risc ridicat' THEN OrdineRisc = 1;
    ELSE IF Risc_Abandon = 'Risc mediu' THEN OrdineRisc = 2;
    ELSE OrdineRisc = 3;

    LABEL Suport_Educational = 'Nivel suport educational'
          Ajutor_Familie     = 'Ajutor familie'
          Meditatii_Private  = 'Meditatii private'
          Meditatii_Scoala   = 'Meditatii la scoala'
          Internet           = 'Are internet acasa'
          Risc_Abandon       = 'Risc de abandon'
          Absente            = 'Numar absente'
          Materii_Picate     = 'Numar materii picate'
          Ore_Studiu         = 'Ore de studiu pe saptamana'
          Medie_Note         = 'Media notelor'
          Eligibil_Bursa     = 'Eligibilitate bursa';

    DROP NrRisc;

RUN;

PROC SORT DATA=proiect.studenti2;
    BY OrdineSuport;
RUN;

TITLE "Analiza suport educational";
PROC PRINT DATA=proiect.studenti2 (OBS=20) LABEL;
    VAR Ajutor_Familie Meditatii_Private 
        Meditatii_Scoala Internet Suport_Educational;
    FORMAT Ajutor_Familie    $yesno_fmt.
           Meditatii_Private $yesno_fmt.
           Meditatii_Scoala  $yesno_fmt.
           Internet          $yesno_fmt.;
RUN;

/* Tabel 2 - risc abandon ordonat ridicat -> mediu -> scazut */
PROC SORT DATA=proiect.studenti2;
    BY OrdineRisc;
RUN;

TITLE "Analiza risc de abandon";
PROC PRINT DATA=proiect.studenti2 (OBS=20) LABEL;
    VAR Suport_Educational Absente 
        Materii_Picate Ore_Studiu Risc_Abandon;
RUN;

/* Tabel 3 - top 30 eligibili bursa ordonati descrescator dupa medie */
PROC SORT DATA=proiect.studenti2;
    BY DESCENDING Medie_Note;
RUN;

TITLE "Top 30 studenti eligibili pentru bursa";
PROC PRINT DATA=proiect.studenti2 (OBS=30) LABEL;
    VAR Nota_T1 Nota_T2 Nota_Finala 
        Medie_Note Eligibil_Bursa;
    WHERE Eligibil_Bursa = 'Eligibil';
RUN;
