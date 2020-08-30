library("rstan")
library("posterior")
library("jsonlite")

options(mc.cores = parallel::detectCores())

rstan_options(auto_write = TRUE)

schools_dat <- list(J = 8,
                    y = c(28,  8, -3,  7, -1,  1, 18, 12),
		    sigma = c(15, 10, 16, 11,  9, 11, 10, 18))

fit <- stan(file = 'Stan-models/8schools.stan', data = schools_dat, chains = 4, iter = 300, warmup = 200, seed=123)

print(fit)

res = extract(fit, permuted=FALSE, inc_warmup=TRUE)
print(dim(res))
write_json(res, "8school_results.json")

print(posterior::summarise_draws(fit))

posterior_summary = posterior::summarise_draws(fit)
print(dim(posterior_summary))
write_json(posterior_summary, "8school_posterior_summary.json")


res_nowarmup = extract(fit, permuted=FALSE, inc_warmup=FALSE)
print(dim(res_nowarmup))
output <- matrix(ncol=17, nrow=dim(res_nowarmup)[3])
j = 0

for (i in 1:dim(res_nowarmup)[3]) {
  ary = matrix(c(res_nowarmup[1:100,1,i], res_nowarmup[1:100,2,i], res_nowarmup[1:100,3,i], res_nowarmup[1:100,4,i]), 100, 4)
  j <- j + 1
  output[j,] <- c(
    posterior::rhat(ary),
    posterior::rhat_basic(ary),
    posterior::ess_bulk(ary),
    posterior::ess_tail(ary),
    posterior::ess_mean(ary),
    posterior::ess_sd(ary),
    posterior::ess_median(ary),
    posterior::ess_basic(ary),
    posterior::ess_quantile(ary, 0.01),
    posterior::ess_quantile(ary, 0.1),
    posterior::ess_quantile(ary, 0.3),
    posterior::mcse_mean(ary),
    posterior::mcse_sd(ary),
    posterior::mcse_median(ary),
    posterior::mcse_quantile(ary, prob=0.01),
    posterior::mcse_quantile(ary, prob=0.1),
    posterior::mcse_quantile(ary, prob=0.3))
}

df = data.frame(output)
colnames(df) <- c("rhat_rank",
                  "rhat_raw",
                  "ess_bulk",
                  "ess_tail",
                  "ess_mean",
                  "ess_sd",
		  "ess_median",
                  "ess_raw",
                  "ess_quantile01",
                  "ess_quantile10",
                  "ess_quantile30",
                  "mcse_mean",
                  "mcse_sd",
		  "mcse_median",
                  "mcse_quantile01",
                  "mcse_quantile10",
                  "mcse_quantile30")
write.csv(df, "reference_posterior.csv")
print(df)
