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

print(c("Seed:", get_seed(fit)))
print(c("Init:", get_inits(fit)))
print(c("Adaptation:", get_adaptation_info(fit)))

print("Chain 1, Draw 1-3")
print(res[1,1:3,])
print(" ")
print("Chain 2, Draw 1-3")
print(res[2,1:3,])
