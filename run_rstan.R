library("rstan")

options(mc.cores = parallel::detectCores())

rstan_options(auto_write = TRUE)

schools_dat <- list(J = 8,
                    y = c(28,  8, -3,  7, -1,  1, 18, 12),
		    sigma = c(15, 10, 16, 11,  9, 11, 10, 18))

fit <- stan(file = 'Stan-models/8schools.stan', data = schools_dat)

print(fit)

df <- as.data.frame(fit)

print(df)

write.csv(df, "8school_results.csv", row.names = FALSE)

print(monitor(fit))
