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
