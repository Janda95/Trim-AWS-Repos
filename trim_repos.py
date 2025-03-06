# Trip repos to minimum survivors using yaml file
# NOTE: if debug is flagged, add each skipped interation to tracking ///////// Normal output will specify name, min survivors
import argparse
import boto3
import json
import logging
import sys
import yaml



HELP = """
    This is the help blurb!
"""


def getArgs(operation="no_help_needed"):
  parser = argparse.ArgumentParser(
    description=HELP
  )
  parser.add_argument(
    "--filename",
    required=True,
    help='Provide yaml file name for ECRs you would like to trim.'
  )
  parser.add_argument(
    "--delete",
    default=False,
    help="Provide permission."
  )
  parser.add_argument(
    "--debug",
    default=False,
    help="Debug will show all interactions: skipped, recommended for deletion, deleted "
  )
  parser.add_argument(
    "--regid",
    default=None,
    help="Debug will show all interactions: skipped, recommended for deletion, "
  )
  if operation == "help":
    parser.print_help()
    sys.exit()

  return parser.parse_args()


def paginateRes(ecrClient, regId, repoNames) -> dict:
  """ Create single json item of paginated response from aws."""
  items = dict()
  nextPage = True
  while nextPage:
    # TODO: update with proper values
    res = ecrClient.describeRepositories(
      registryId=regId,
      repositoryNames= repoNames,
      nextToken="TrimReposToMinWithTtyl",
    )

    res = json.loads(res)

    # load into dict items

    # if not nextToken:
    #   nextPage = False

    # res none
    if res is None:
      print("No repos available with requested names.")
      sys.exit(0)


def trim(fileName: str, debug: bool, canDelete: bool, regId: str):
  """Load, sort, check, and remove extra repo instances."""
  try:
    file = open(fileName, mode="rb")
  except OSError:
    print( f"Could not open/read file: {fileName}")
    sys.exit()

  with file:
    contents = yaml.safe_load(file)
  
  ecrClient = boto3.client("ecr")

  reposToRequest = list()

  # check for expected structure
  for group in contents.get("ECRs"):
    name = group.get("name", None)
    minAgeHours = group.get("minAgeHours", None)
    minSurvivors = group.get("minSurvivors", None)

    if debug is True:
          msg = f"Name: {name}, MinAgeHours: {minAgeHours}, and Survivors: {minSurvivors}"
          logger.info(msg)

    if name is not None:
      reposToRequest.append( (name, minAgeHours, minSurvivors) )

  allRepos = paginateRes( ecrClient, map(lambda x: x[0], reposToRequest))

  for name, minAgeHours, minSurvivors in reposToRequest:
    activeRepos = allRepos.get(name, None)

    if len(activeRepos) <= minSurvivors:
      if debug is True:
        msg = "Repos: " + str(activeRepos) + " don't need to be trimmed."
        logging.info(msg)
      continue

    # iterate through items, create list with important info, sort by datetime (oldest to newest)
    # trim with range, outside of range are skipped 
    # iterate through list and request kill of any older than min_age_hours


def main():
  args = getArgs()
  trim(args.filename, args.debug, args.delete, args.regid)


if __name__ == "__main__":
  logger = logging.getLogger(__name__)
  logger.info("Started")
  main()
  logger.info("Finished")
