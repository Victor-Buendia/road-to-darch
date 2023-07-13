from utils.misc import deep_get


class TimeEntry:
    def __init__(
        self, id, description, start_timestamp, end_timestamp, duration, project_id
    ):
        self.encoding_format = "utf-8"
        self.id = id
        self.duration = duration
        self.project_id = project_id
        self.description = description
        self.end_timestamp = end_timestamp
        self.start_timestamp = start_timestamp
        self.duration_minutes = self.get_duration_in_minutes()

    def __str__(self):
        return f"Time Entry: {self.id} - Minutes: {self.duration_minutes} - Description: {self.description} - StartTimestamp: {self.start_timestamp}"

    def get_duration_in_minutes(self):
        return round(self.duration / 60.0, 2)

    def encoded_string(string):
        return bytes(str(string), "utf-8").decode("utf-8")

    @property
    def insert_tuple(self):
        insert_tuple = (
            self.id,
            self.duration,
            self.project_id,
            self.description,
            self.end_timestamp,
            self.start_timestamp,
            self.duration_minutes,
        )

        return insert_tuple

    @classmethod
    def from_api_object_list(cls, object_list):
        time_entries = object_list.get("timeentries")

        objects = []
        for entry in time_entries:
            data = [
                deep_get(entry, "_id"),
                cls.encoded_string(deep_get(entry, "description")),
                deep_get(entry, "timeInterval.start"),
                deep_get(entry, "timeInterval.end"),
                deep_get(entry, "timeInterval.duration"),
                cls.encoded_string(deep_get(entry, "projectId")),
            ]
            objects.append(cls(*data))

        return objects
