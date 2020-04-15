import pystan

schools_dat = dict(
    J = 8,
    y = [28,  8, -3,  7, -1,  1, 18, 12],
    sigma = [15, 10, 16, 11,  9, 11, 10, 18]
)

model = pystan.StanModel(file="Stan-models/8schools.stan", extra_compile_args=['-O3'])

fit = model.sampling(data=schools_dat, chains=2, iter=300, warmup=200, seed=123)

res = fit.extract(permuted=False)

print("Seed:", fit.get_seed())
print("Init:", fit.get_inits())
print("Adaptation:", fit.get_adaptation_info())

print("Chain 1, Draw 1-3")
print(list(res[:3,0,:]))
print(" ")
print("Chain 2, Draw 1-3")
print(list(res[:3,1,:]))
