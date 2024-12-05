### *Under Construction*

# TrimExtraRepos_Lambda

### Overview
AWS Lambda to comb through running repo instances and kill off oldest survivors up to Min Survivors that have passed Time To Live


### Progress and Planned Updates
- [ ] Generate Testing Environment
- [ ] Local Testing
- [ ] Lambda testing
- [ ] Tested and approved

### Input:
- yaml file with expected parameters:
  - repo_name
  - ttl_hours
  - min_survivors

### Output
- Debug output showing every skipped interaction
- Regular output to python logger showing trimming of oldest repos past expected EOL
