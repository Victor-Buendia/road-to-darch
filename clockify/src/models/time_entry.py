class TimeEntry:
	def __init__(self, id, description, start_timestamp, end_timestamp, duration, project_id):
		self.id = id
		self.description = description
		self.start_timestamp = start_timestamp
		self.end_timestamp = end_timestamp
		self.duration = duration
		self.project_id = project_id

	def __str__(self):
		return f'Time Entry: {self.id}'

	@classmethod
	def from_api_object_list(cls, object_list):
		time_entries = object_list.get("timeentries")

		objects = []
		for entry in time_entries:
			data = [
				entry.get("_id"),
				entry.get("description"),
				entry.get("start_timestamp"),
				entry.get("end_timestamp"),
				entry.get("duration"),
				entry.get("project_id")
			]
			objects.append(cls(*data))

		return objects