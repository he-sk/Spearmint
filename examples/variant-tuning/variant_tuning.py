import sqlite3, numpy

# configuration
my_config = {
    "name": "frog1.cpu",
    "db": sqlite3.connect("frog1.cpu.db"),
    "groups": 1,
    "measurement": "Kernel"
}


def variant_tuning(algorithm, memory_access, multiplier, local_size):
    # fix parameters
    algorithm = ["shared", "independent", "local"][algorithm]
    memory_access = ["sequential", "coalesced"][memory_access]
    multiplier = 2 ** multiplier
    local_size = 2 ** local_size

    # get measurement data
    query = """SELECT mean_runtime_ms, sd_runtime_ms, min_runtime_ms, max_runtime_ms
FROM measurements
WHERE measurement = ?
AND groups = ?
AND algorithm = ?
AND memory_access = ?
AND multiplier = ?
AND local_size = ?"""
    result = my_config["db"].execute(query,
                                     (my_config["measurement"], my_config["groups"],
                                      algorithm, memory_access, multiplier, local_size)).fetchone()
    if result:
        _mean, _sd, _min, _max = result
        print "Measurement for %s, groups = %d, algorithm = %s, memory_access = %s, multiplier = %d, local_size = %d: mean = %.3f, sd = %.3f, min = %.3f, max = %.3f" % (
            my_config["name"], my_config["groups"], algorithm, memory_access, multiplier, local_size, _mean, _sd, _min,
            _max)

    # simulate measurement
    runtime_ms, = numpy.random.normal(_mean, _sd, 1)
    if runtime_ms < 0:
        print "Simulated runtime is negative: %.3f; mean = %.3f, sd = %.3f; clipping to measured minimum: %.3f" % (
            runtime_ms, _mean, _sd, _min)
        runtime_ms = _min
    if runtime_ms < _mean - 5 * _sd:
        print "Simulated runtime is too low: %.3f; mean = %.3f, sd = %.3f; clipping to measured minimum: %.3f" % (
            runtime_ms, _mean, _sd, _min)
        runtime_ms = _min
    elif runtime_ms > _mean + 5 * _sd:
        print "Simulated runtime is too high: %.3f; mean = %.3f, sd = %.3f; clipping to measured maximum: %.3f" % (
            runtime_ms, _mean, _sd, _max)
    runtime_ms = _max
    print "Measurement for mean = %.3f, sd = %.3f: %.3f" % (_mean, _sd, runtime_ms)
    return runtime_ms


# Write a function like this called 'main'
def main(job_id, params):
    return variant_tuning(params['algorithm'][0], params['memory_access'][0], params['multiplier'][0],
                          params['local_size'][0])
