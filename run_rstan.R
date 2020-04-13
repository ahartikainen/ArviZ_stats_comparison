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
print(dim(res))
write_json(res, "8school_results.json")

print(monitor(fit))

res_monitor = monitor(fit)
print(dim(res_monitor))
write_json(res_monitor, "8school_results_monitor.json")


res_nowarmup = extract(fit, permuted=FALSE, inc_warmup=FALSE)
print(dim(res_nowarmup))
output <- matrix(ncol=15, nrow=dim(res_nowarmup)[3])
j = 0

for (i in 1:dim(res_nowarmup)[3]) {
  ary = matrix(c(res_nowarmup[1:100,1,i], res_nowarmup[1:100,2,i], res_nowarmup[1:100,3,i], res_nowarmup[1:100,4,i]), 100, 4)
  j <- j + 1
  output[j,] <- c(
    rstan:::rhat(ary),
    rstan:::rhat_rfun(ary),
    rstan:::ess_bulk(ary),
    rstan:::ess_tail(ary),
    rstan:::ess_mean(ary),
    rstan:::ess_sd(ary),
    rstan:::ess_rfun(ary),
    rstan:::ess_quantile(ary, 0.01),
    rstan:::ess_quantile(ary, 0.1),
    rstan:::ess_quantile(ary, 0.3),
    rstan:::mcse_mean(ary),
    rstan:::mcse_sd(ary),
    rstan:::mcse_quantile(ary, prob=0.01),
    rstan:::mcse_quantile(ary, prob=0.1),
    rstan:::mcse_quantile(ary, prob=0.3))
}

df = data.frame(output)
colnames(df) <- c("rhat_rank",
                  "rhat_raw",
                  "ess_bulk",
                  "ess_tail",
                  "ess_mean",
                  "ess_sd",
                  "ess_raw",
                  "ess_quantile01",
                  "ess_quantile10",
                  "ess_quantile30",
                  "mcse_mean",
                  "mcse_sd",
                  "mcse_quantile01",
                  "mcse_quantile10",
                  "mcse_quantile30")
write.csv(df, "reference_values.csv")
print(df)
