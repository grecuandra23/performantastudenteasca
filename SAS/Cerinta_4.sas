LIBNAME proiect '/home/u64505510/Proiect';

DATA proiect.studenti_GP;
    SET proiect.studenti2;
    IF Scoala = 'GP';
RUN;

DATA proiect.studenti_MS;
    SET proiect.studenti2;
    IF Scoala = 'MS';
RUN;

DATA proiect.studenti_Rural;
    SET proiect.studenti2;
    IF Mediu = 'R';
RUN;

DATA proiect.studenti_Urban;
    SET proiect.studenti2;
    IF Mediu = 'U';
RUN;

TITLE "Studenti scoala GP";
PROC PRINT DATA=proiect.studenti_GP (OBS=30) LABEL;
    VAR Sex Varsta Mediu Ore_Studiu Materii_Picate
        Meditatii_Scoala Ajutor_Familie Meditatii_Private
        Internet Relatie Timp_Liber Iesiri
        Alcool_Saptamana Alcool_Weekend Absente
        Nota_T1 Nota_T2 Nota_Finala
        Promovabilitate Suport_Educational
        Risc_Abandon Medie_Note Eligibil_Bursa;
RUN;

TITLE "Studenti scoala MS";
PROC PRINT DATA=proiect.studenti_MS (OBS=30) LABEL;
    VAR Sex Varsta Mediu Ore_Studiu Materii_Picate
        Meditatii_Scoala Ajutor_Familie Meditatii_Private
        Internet Relatie Timp_Liber Iesiri
        Alcool_Saptamana Alcool_Weekend Absente
        Nota_T1 Nota_T2 Nota_Finala
        Promovabilitate Suport_Educational
        Risc_Abandon Medie_Note Eligibil_Bursa;
RUN;

TITLE "Studenti din mediul rural";
PROC PRINT DATA=proiect.studenti_Rural (OBS=30) LABEL;
    VAR Scoala Sex Varsta Ore_Studiu Materii_Picate
        Meditatii_Scoala Ajutor_Familie Meditatii_Private
        Internet Relatie Timp_Liber Iesiri
        Alcool_Saptamana Alcool_Weekend Absente
        Nota_T1 Nota_T2 Nota_Finala
        Promovabilitate Suport_Educational
        Risc_Abandon Medie_Note Eligibil_Bursa;
RUN;

TITLE "Studenti din mediul urban";
PROC PRINT DATA=proiect.studenti_Urban (OBS=30) LABEL;
    VAR Scoala Sex Varsta Ore_Studiu Materii_Picate
        Meditatii_Scoala Ajutor_Familie Meditatii_Private
        Internet Relatie Timp_Liber Iesiri
        Alcool_Saptamana Alcool_Weekend Absente
        Nota_T1 Nota_T2 Nota_Finala
        Promovabilitate Suport_Educational
        Risc_Abandon Medie_Note Eligibil_Bursa;
RUN;

DATA proiect.studenti_SuportComplet;
    SET proiect.studenti2;
    IF Suport_Educational = 'Suport complet';
RUN;

DATA proiect.studenti_SuportPartial;
    SET proiect.studenti2;
    IF Suport_Educational = 'Suport partial';
RUN;

DATA proiect.studenti_FaraSuport;
    SET proiect.studenti2;
    IF Suport_Educational = 'Fara suport';
RUN;

TITLE "Studenti cu suport educational complet";
PROC PRINT DATA=proiect.studenti_SuportComplet (OBS=30) LABEL;
    VAR Scoala Sex Varsta Ajutor_Familie 
        Meditatii_Private Meditatii_Scoala 
        Internet Suport_Educational Nota_Finala;
RUN;

TITLE "Studenti cu suport educational partial";
PROC PRINT DATA=proiect.studenti_SuportPartial (OBS=30) LABEL;
    VAR Scoala Sex Varsta Ajutor_Familie 
        Meditatii_Private Meditatii_Scoala 
        Internet Suport_Educational Nota_Finala;
RUN;

TITLE "Studenti fara suport educational";
PROC PRINT DATA=proiect.studenti_FaraSuport (OBS=30) LABEL;
    VAR Scoala Sex Varsta Ajutor_Familie 
        Meditatii_Private Meditatii_Scoala 
        Internet Suport_Educational Nota_Finala;
RUN;
