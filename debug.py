from jobParser import JobParser, JobParserDB


test_db = JobParserDB(table_name="sterlitamak")

j = test_db.db_get_all_active_jobs()

print(j)
