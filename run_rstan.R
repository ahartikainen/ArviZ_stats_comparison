library("rstan")
library("jsonlite")

options(mc.cores = parallel::detectCores())

rstan_options(auto_write = TRUE)

schools_dat <- list(J = 8,
                    y = c(28,  8, -3,  7, -1,  1, 18, 12),
		    sigma = c(15, 10, 16, 11,  9, 11, 10, 18))

fit <- stan(file = 'Stan-models/8schools.stan', data = schools_dat, chains = 4, iter = 300, warmup = 200)

print(fit)

res = extract(fit, permuted=FALSE, inc_warmup=TRUE)
write_json(res, "8school_results.json")

print(monitor(fit))

res_monitor = monitor(fit)
write_json(res_monitor, "8school_results_monitor.json")
