# === URLS ===
LESSONS_URL = "https://obs.itu.edu.tr/public/DersProgram"
COURSES_URL = "https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-bilgileri/ders-bilgileri.php"
COURSE_PLAN_URLS = [
    "https://obs.itu.edu.tr/public/DersPlan/DersPlanlariList?programKodu={0}_LS&planTipiKodu=lisans",       # Undergraduate
    "https://obs.itu.edu.tr/public/DersPlan/DersPlanlariList?programKodu={0}_LS&planTipiKodu=uolp",         # UOLP
    "https://obs.itu.edu.tr/public/DersPlan/DersPlanlariList?programKodu={0}_OL&planTipiKodu=on-lisans",    # Graduate
]
BUILDING_CODES_URL = "https://www.sis.itu.edu.tr/TR/obs-hakkinda/bina-kodlari.php"
PROGRAMME_CODES_URL = "https://www.sis.itu.edu.tr/TR/obs-hakkinda/lisans-program-kodlari.php"
FINAL_EXAM_URL = "https://obs.itu.edu.tr/public/FinalTakvimi/FinalTakvimiByDersBransKodu"

# === FILE NAMES ===
LESSONS_FILE_PATH = "data/lessons.psv"
COURSES_FILE_PATH = "data/courses.psv"
COURSE_PLANS_FILE_PATH = "data/course_plans.txt"
BUILDING_CODES_FILE_PATH = "data/building_codes.psv"
PROGRAMME_CODES_FILE_PATH = "data/programme_codes.psv"
FINAL_EXAMS_FILE_PATH = "data/final_exams.psv"

# === OTHER ===
MAX_THREAD_COUNT = 4
