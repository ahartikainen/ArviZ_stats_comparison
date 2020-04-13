library("rstan")

options(mc.cores = parallel::detectCores())

rstan_options(auto_write = TRUE)

schools_dat <- list(J = 8,
                    y = c(28,  8, -3,  7, -1,  1, 18, 12),
		    sigma = c(15, 10, 16, 11,  9, 11, 10, 18))

fit <- stan(file = 'Stan-models/8schools.stan', data = schools_dat)

print(fit)

print(as.data.frame(fit))

write.csv(as.data.frame(fit), "8school_results.csv", row.names = FALSE)
