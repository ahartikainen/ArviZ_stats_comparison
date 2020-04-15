import arviz as az
import pystan

schools_dat = dict(
    J = 8,
    y = [28,  8, -3,  7, -1,  1, 18, 12],
    sigma = [15, 10, 16, 11,  9, 11, 10, 18]
)

model = pystan.StanModel(file="Stan-models/8schools.stan", extra_compile_args=['-O3'])

fit = model.sampling(data=schools_dat, chains=4, iter=300, warmup=200, seed=123)

print(fit)

print(az.summary(fit))

print(fit.extract(permuted=False))
