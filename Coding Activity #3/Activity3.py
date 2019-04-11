

def definite_integral(samples, lower_limit, upper_limit, sampling_period):
    if lower_limit == upper_limit:
        return 0.0
    else:
        area = 0.5 * (samples[lower_limit] + samples[upper_limit])
        i = lower_limit + 1
        while i < upper_limit:
            area = area + samples[i]
            i += 1
        return sampling_period * area


def sampleIntegral(samples, sampling_period):
    if len(samples) < 2:
        return 0.0
    area = 0.5 * samples[0]
    i = 1
    while i < len(samples) - 1:
        area = area + samples[i]
        i += 1
    area = area + 0.5 * samples[i]
    return area * sampling_period
