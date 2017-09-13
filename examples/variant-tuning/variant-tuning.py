import numpy as np
import math
import psycopg2

def variant_tuning(workgroups, local_size, memory_access, bitmap_granularity):

    db = psycopg2.connect("dbname='experiments'").cursor()
    experiment_id = '2016-06-14.91' # subselect_float on Radeon Fury R9
    num_cus = 56
    query = """SELECT runtime_ns FROM data_exhaustive_evaluation_3
               WHERE experiment_id = '%s'
               AND   workgroups = %s * %s
               AND   local_size = %s
               AND   memory_access = %s
               AND   bitmap_granularity = %s""" % (experiment_id, workgroups[0], num_cus, local_size[0], memory_access[0], bitmap_granularity[0])
    print query
    db.execute(query)
    if db.rowcount == 1:
        result = db.fetchone()[0]
    else:
        result = np.nan
    
    print 'Result = %f' % result
    #time.sleep(np.random.randint(60))
    return result

# Write a function like this called 'main'
def main(job_id, params):
    print 'Anything printed here will end up in the output directory for job #%d' % job_id
    print params
    return variant_tuning(params['workgroups'], params['local_size'], params['memory_access'], params['bitmap_granularity'])
