import requests as r
import json
import pprint
import os

from aws.ssm import ParameterStoreFetcher

class Interactor:
	def __init__(self, workspace_id):
		self.__fetcher = ParameterStoreFetcher('us-east-1')
		self.__api_key = self.__fetcher.fetch_parameter_value('prd-credentials.clockify.api-key')
		self.__workspace_id = workspace_id

	@property
	def base_endpoint(self):
		return (f'https://reports.api.clockify.me/v1/workspaces/{self.__workspace_id}')

	@property
	def detailed_reports_endpoint(self):
		return (os.path.join(self.base_endpoint.strip('/'), 'reports/detailed'))


workspace_id = '5e95c064ea8094116e8e0a56'

# header = {
#     'x-api-key': api_key
#     , 'content-type': 'application/json'
# }

# response = json.loads(r.post(url=f'https://reports.api.clockify.me/v1/workspaces/{workspace_id}/reports/detailed'
#                              , headers=header
#                              , json={
#                                  'dateRangeStart': '2023-01-10T00:00:00.000Z'
#                                  , 'dateRangeEnd': '2023-01-21T00:00:00.000Z'
#                                  , "detailedFilter": {}
#                              }).text)
# pprint.pprint(response)

a = Interactor(workspace_id)
print(a.base_endpoint)
print(a.detailed_reports_endpoint)
print(a.api_key)