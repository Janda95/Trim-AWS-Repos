# Trip repos to minimum survivors using yaml file
# NOTE: if debug is flagged, add each skipped interation to tracking ///////// Normal output will specify name, min survivors
import sys
# import boto3
import yaml
import logging
import argparse


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


def trim(file_name):
  # load contents
  try:
    file = open(file_name, mode="rb")
  except OSError:
    print( f"Could not open/read file: {file_name}")
    sys.exit()

  with file:
    contents = yaml.safe_load(file)

  # check for expected structure
  for group in contents.get('ECRs'):
    name = group.get('name', None)
    min_age_hours = group.get('min_age_hours', None)
    min_survivors = group.get('min_survivors', None)

    msg = f"name: {name}, min_age_hours: {min_age_hours}, and survivors: {min_survivors}"
    print(msg)

    aws_items = list() # replace with aws query for items attatched to ECR with ids

    if len(aws_items) <= min_survivors:
      # if debug, specify skipped items due to survivors
      continue

    # query additional information about items using ids
    aws_items_with_info = list()

    # iterate through items, create list with important info, sort by datetime (oldest to newest)
    # trim with range, outside of range are skipped 
    # iterate through list and request kill of any older than min_age_hours


def main():
  args = get_args()
  # get_args(operation='help')
  trim(args.filename, args.debug, args.delete)


def handler(event, context):
  args = get_args()
  # get_args(operation='help')
  trim(args.filename, args.debug, args.delete)


if __name__ == '__main__':
  # main()
  logger.info(handler(1,1))
