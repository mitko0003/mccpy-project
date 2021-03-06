import numpy as np
import scipy.stats

def bhatt_d(p, q):
    return np.sqrt(1 - sum(np.sqrt(p*q)))

def per_color_bhatt_d(ps, qs):
    # ps and qs contains per color histogram
    distances = []
    for i in range(len(ps)):
        distances.append(sum(np.sqrt(ps[i] * qs[i])))
    distance = (sum(distances) / len(distances))[0]
    return np.sqrt(1 - distance)


def get_weights(target_hist, particle_set_hists, sigma=0.1):
    # default value is empirically chosen
    norm = scipy.stats.norm(0, sigma)
    relative_weights = [norm.pdf(per_color_bhatt_d(target_hist, particle_hist))
            for particle_hist in particle_set_hists]
    relative_weights = np.asarray(relative_weights)
    return relative_weights / sum(relative_weights)

def estimate(weights, particles):
    return sum(particles * weights[:, np.newaxis])

def adapt_target(target, estimate, alpha):
    """ target from step t, estimate for t+1 """
    return (1 - alpha) * target + alpha * estimate

def should_update_target(target, estimate, n, sigma=0.1):
    return bhatt_d(target, estimate) < n * sigma
