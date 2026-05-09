LIBNAME proiect '/home/u64501251/Proiect';

PROC FORMAT;
    VALUE $sex_fmt   
        'M' = 'Masculin'   
        'F' = 'Feminin';

    VALUE $mediu_fmt 
        'U' = 'Urban'   
        'R' = 'Rural';

    VALUE $yesno_fmt  
        'yes' = 'Da'
        'no'  = 'Nu';

    VALUE frecventa_fmt
        1 = 'Foarte rar'
        2 = 'Rar'
        3 = 'Ocazional'
        4 = 'Des'
        5 = 'Foarte des';
RUN;

DATA proiect.studenti;
    INFILE '/home/u64501251/Proiect/student_procesat.csv' DSD FIRSTOBS=2;
    INPUT Scoala    $
          Sex       $
          Varsta
          Mediu     $
          Ore_Studiu
          Materii_Picate
          Meditatii_Scoala  $
          Ajutor_Familie    $
          Meditatii_Private $
          Internet          $
          Relatie           $
          Timp_Liber
          Iesiri
          Alcool_Saptamana
          Alcool_Weekend
          Absente
          Nota_T1
          Nota_T2
          Nota_Finala;

	length Promovabilitate $ 11;
    IF Nota_Finala >= 10 THEN Promovabilitate = 'Promovat';
    ELSE Promovabilitate = 'Nepromovat';

    LABEL Scoala             = 'Scoala'
          Sex                = 'Genul studentului'
          Varsta             = 'Varsta studentului'
          Mediu              = 'Mediul de provenienta'
          Ore_Studiu         = 'Ore de studiu pe saptamana'
          Materii_Picate     = 'Numar materii picate'
          Meditatii_Scoala   = 'Meditatii la scoala'
          Ajutor_Familie     = 'Ajutor din partea familiei'
          Meditatii_Private  = 'Meditatii private'
          Internet           = 'Are internet acasa'
          Relatie            = 'Are o relatie'
          Timp_Liber         = 'Timp liber'
          Iesiri             = 'Frecventa iesirilor'
          Alcool_Saptamana   = 'Consum alcool in timpul saptamanii'
          Alcool_Weekend     = 'Consum alcool in weekend'
          Absente            = 'Numar absente'
          Nota_T1            = 'Nota primul test'
          Nota_T2            = 'Nota al doilea test'
          Nota_Finala        = 'Nota finala'
          Promovabilitate    = 'Status promovare';

    FORMAT Sex                $sex_fmt.
           Mediu              $mediu_fmt.
           Meditatii_Scoala   $yesno_fmt.
           Ajutor_Familie     $yesno_fmt.
           Meditatii_Private  $yesno_fmt.
           Internet           $yesno_fmt.
           Relatie            $yesno_fmt.
           Iesiri             frecventa_fmt.
           Alcool_Saptamana   frecventa_fmt.
           Alcool_Weekend     frecventa_fmt.;
RUN;

TITLE "Date studenti portughezi";
PROC PRINT DATA=proiect.studenti (OBS=10) LABEL;
RUN;