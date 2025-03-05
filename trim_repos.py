# Trip repos to minimum survivors using yaml file
# NOTE: if debug is flagged, add each skipped interation to tracking ///////// Normal output will specify name, min survivors
import argparse
import boto3
import logging
import sys
import yaml


HELP = '''
    This is the help blurb!
'''


def get_args(operation='no_help_needed'):
  parser = argparse.ArgumentParser(
    description=HELP
  )
  parser.add_argument(
    '--filename',
    required=True,
    help='Provide yaml file name for ECRs you would like to trim.'
  )
  parser.add_argument(
    '--delete',
    default=False,
    help='Provide permission'
  )
  parser.add_argument(
    '--debug',
    default=False,
    help="Debug will show all interactions: skipped, recommended for deletion, deleted "
  )
  if operation == 'help':
    parser.print_help()
    sys.exit()

  return parser.parse_args()


def trim(file_name: str, ecr_name: str ):
  # load contents
  try:
    file = open(file_name, mode="rb")
  except OSError:
    print( f"Could not open/read file: {file_name}")
    sys.exit()

  with file:
    contents = yaml.safe_load(file)
  
  ecr_client = boto3.client(ecr_name)

  repos_to_request = list()

  # check for expected structure
  for group in contents.get("ECRs"):
    name = group.get("name", None)
    min_age_hours = group.get("min_age_hours", None)
    min_survivors = group.get("min_survivors", None)

    # if parser.debug == True:
        #   msg = f"name: {name}, min_age_hours: {min_age_hours}, and survivors: {min_survivors}"
        #   print(msg)

    if name != None:
      repos_to_request.append( (name, min_age_hours, min_survivors) )    
    

  # TODO: update with proper values
  res = ecr_client.describeRepositories(
    registryId='string',
    repositoryNames=[
        'string',
    ],
    nextToken='string',
    maxResults=123
  ).get('repositories', None)

  if res == None:
    print(f"No repos available with requested names.")
    sys.exit(0)
    
    # for group_of_repos in res.repos

  for name, min_age_hours, min_survivors in repos_to_request:
    active_repos = res.get(name, None)


    if len(active_repos) <= min_survivors:
      if parser.debug == True: 
        print(active_repos)
      
      continue

    # iterate through items, create list with important info, sort by datetime (oldest to newest)
    # trim with range, outside of range are skipped 
    # iterate through list and request kill of any older than min_age_hours


def main():
  args = get_args()
  trim(args.filename, 'ecr')


if __name__ == '__main__':
  main()
