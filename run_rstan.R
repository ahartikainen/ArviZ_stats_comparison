library("rstan")
library("jsonlite")

options(mc.cores = parallel::detectCores())
rstan_options(auto_write = TRUE)

schools_dat <- list(
    J = 8,
    y = c(28,  8, -3,  7, -1,  1, 18, 12),
		sigma = c(15, 10, 16, 11,  9, 11, 10, 18))

fit <- stan(file = 'Stan-models/8schools.stan', data = schools_dat, chains = 2, iter = 300, warmup = 200, seed=123)

res = extract(fit, permuted=FALSE, inc_warmup=FALSE)

print("################### SEED ###################")
print(get_seed(fit))
print("################### INIT ###################")
print(get_inits(fit)))
print("################ ADAPTATION ################")
print(get_adaptation_info(fit))


print("##### Chain 1, Draw 1-3 #####")
print(res[1:3,1,])
print(" ")
print("##### Chain 2, Draw 1-3 #####")
print(res[1:3,2,])
