
data {
  int<lower=0> N;
  real y[N];
  vector[N] x;
}

parameters {
  real beta;
  real alpha;
  real<lower=0> sigma;
}

model {
  beta ~ normal(3.2,10^2);
  y ~ normal(alpha + beta * (x-1970), sigma);
}

generated quantities{
  vector[N] log_lik;
  vector[N] y_rep;
 
 for (i in 1:N) {
   log_lik[i] = normal_lpdf(y[i] | alpha + beta * (x[i]-1970), sigma);
   y_rep[i] = normal_rng(alpha + beta * (x[i]-1970), sigma);
 }
}