data {
  int N;
  vector[N] y;
  vector[N] x;
  int k;
  int i[N];
}

parameters {
  vector[k] beta;
  vector[k] alpha;
  vector<lower=0>[k] sigma;
  real sigma0;
  real beta0;
}

model {
  beta0 ~ normal(3.2,10^2);
  sigma0 ~ normal(0, 10);
  beta ~ normal(beta0, sigma0);
  y ~ normal(alpha[i] + beta[i] .* (x-1970), sigma[i]);
}

generated quantities{
  vector[N] log_lik;
  vector[N] y_rep;
 
 for (j in 1:N) {
   log_lik[j] = normal_lpdf(y[j] | alpha[i[j]] + beta[i[j]] .* (x[j]-1970), sigma[i[j]]);
   y_rep[j] = normal_rng(alpha[i[j]] + beta[i[j]] .* (x[j]-1970), sigma[i[j]]);
 }
}
