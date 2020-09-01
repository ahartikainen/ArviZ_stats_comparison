library("rstan")
library("posterior")
library("jsonlite")

options(mc.cores = parallel::detectCores())
options(digits=16)

rstan_options(auto_write = TRUE)

print(Sys.getenv())
print(Sys.getenv(x = "USEGIT"))
print(Sys.getenv(x = "USEGIT") == "true")
print(Sys.getenv(x = "USEGIT") == "false")
print(Sys.getenv(x = "USEGIT") == TRUE)
print(Sys.getenv(x = "USEGIT") == FALSE)
if (Sys.getenv(x = "USEGIT") == "true") {
  env_name <- "git"
} else {
    env_name <- "pypi-cran"
}
print(env_name)

schools_dat <- list(J = 8,
                    y = c(28,  8, -3,  7, -1,  1, 18, 12),
		    sigma = c(15, 10, 16, 11,  9, 11, 10, 18))
fit <- stan(file = 'Stan-models/8schools.stan', data = schools_dat, chains = 4, iter = 300, warmup = 200, seed=123)
print(fit)


res = extract(fit, permuted=FALSE, inc_warmup=TRUE)
print("Dim res")
print(dim(res))
write_json(res, paste(paste("8school_results", env_name, sep="_", collapse=""), ".json", sep=""), digits=16)

res_nowarmup <- extract(fit, permuted=FALSE, inc_warmup=FALSE)
print("Dim res no warmup")
print(dim(res_nowarmup))
write_json(res_nowarmup, paste(paste("8school_results_nowarmup", env_name, sep="_", collapse=""), ".json", sep=""), digits=16)

res_nowarmup_reread <- read_json(paste(paste("8school_results_nowarmup", env_name, sep="_", collapse=""), ".json", sep=""))
res_nowarmup_reread <- aperm(array(unlist(res_nowarmup_reread), rev(dim(res_nowarmup))))

print("Dim res no warmup reread")
print(dim(res_nowarmup_reread))

print("difference between original and loaded < 1e-10")
print(all(abs(res_nowarmup - res_nowarmup_reread) < 1e-10))
print(res_nowarmup - res_nowarmup_reread)

posterior_summary = posterior::summarise_draws(fit)
print(dim(posterior_summary))
print(posterior_summary)
write_json(posterior_summary, paste(paste("posterior_summary", env_name, sep="_", collapse=""), ".json", sep=""), digits=16)


output <- matrix(ncol=17, nrow=dim(res_nowarmup_reread)[3])
j = 0
for (i in 1:dim(res_nowarmup_reread)[3]) {
  ary = matrix(c(res_nowarmup_reread[1:100,1,i], res_nowarmup_reread[1:100,2,i], res_nowarmup_reread[1:100,3,i], res_nowarmup_reread[1:100,4,i]), 100, 4)
  j <- j + 1
  output[j,] <- c(
    posterior::rhat(ary),
    posterior::rhat_basic(ary, FALSE),
    posterior::ess_bulk(ary),
    posterior::ess_tail(ary),
    posterior::ess_mean(ary),
    posterior::ess_sd(ary),
    posterior::ess_median(ary),
    posterior::ess_basic(ary, FALSE),
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
write.csv(df, paste(paste("reference_posterior", env_name, sep="_", collapse=""), ".csv", sep=""))

print(df)
