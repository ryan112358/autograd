from __future__ import absolute_import

import autograd.numpy as np
import scipy.stats

from autograd.core import primitive
from autograd.numpy.numpy_grads import unbroadcast

cdf = primitive(scipy.stats.poisson.cdf)
logpmf = primitive(scipy.stats.poisson.logpmf)
pmf = primitive(scipy.stats.poisson.pmf)

def grad_poisson_logpmf(k, mu):
    return np.where(k % 1 == 0, k / mu - 1, 0)

cdf.defvjp(lambda g, ans, vs, gvs, k, mu: unbroadcast(vs, gvs, g * -pmf(np.floor(k), mu)), argnum=1)
logpmf.defvjp(lambda g, ans, vs, gvs, k, mu: unbroadcast(vs, gvs, g * grad_poisson_logpmf(k, mu)), argnum=1)
pmf.defvjp(lambda g, ans, vs, gvs, k, mu: unbroadcast(vs, gvs, g * ans * grad_poisson_logpmf(k, mu)), argnum=1)
