locals {
  stack_name = "amc"
  client = var.client
  environment = var.environment
  region = var.region
  account_id = var.account_id
  amc_project_env = {
    sandbox = "SANDBOX"
    staging = "STAGING"
    development = "DEVELOPMENT"
    production = "PRODUCTION"
  }
  processed_amc_data_table_name = "processed_amc_data"
  amc_eb_payloads_bucket_name = "${local.client}-${local.environment}-amc-eb-payloads"
}
