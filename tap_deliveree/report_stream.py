import singer 
from singer.catalog import CatalogEntry
from singer.schema import Schema
from singer.metrics import http_request_timer
import backoff
import requests
from .utils import parse_parameters

LOGGER = singer.get_logger()

class ReportStream:
  def __init__(self, report) -> None:
    self.report = report

  def get_key_properties(self):
    return self.report["key_properties"]

  def generate_schema(self):
    schema = dict()
    schema["title"] = self.report["name"]
    schema["type"] = ["null", "object"]
    properties = dict()
    schema["properties"] = properties
    for property in self.report["properties"]:
      types = [property["type"]]
      if property.get("nullable") is True:
        types.append("null")

      properties[property["name"]] = {"type": types}

    # Add data property
    properties["data"] = {
      "type": ["null", "object"],
    }

    return schema

  def generate_catalog_entry(self):
    stream = self.report["name"]
    schema = self.generate_schema()
    key_properties = self.report["key_properties"]
    metadata = singer.metadata.get_standard_metadata(
        schema=schema,
        key_properties=key_properties,
        valid_replication_keys=key_properties,
        replication_method="INCREMENTAL"
      )

    return CatalogEntry(tap_stream_id=stream, stream=stream, schema=Schema.from_dict(schema), metadata=metadata)

  def write_schema(self):
    schema = self.generate_schema()
    key_properties = self.report["key_properties"]
    return singer.write_schema(stream_name=self.report["name"], schema=schema, key_properties=key_properties)

  @backoff.on_exception(backoff.expo, Exception, max_tries=5, factor=2)
  def get_data(self, config):
    url = f"{config['base_url']}/{config['resource']}/{self.report['name']}"
    LOGGER.debug(f"Sending request to URL: {url}")
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Basic {config['api_key']}"
    }

    parameters = parse_parameters(self.report["parameters"])
    response = requests.get(url, headers=headers, params=parameters)
    response.raise_for_status()

    return response.json(), parameters

  def get_records(self, config):
    
    with http_request_timer(self.report["name"]):
      data, parameters = self.get_data(config)
      
    records = []
    for entry in data:
      record = dict()
      for property in self.report["properties"]:
        record[property["name"]] = entry[property["name"]]
      record["data"] = entry
      records.append(record)
    return records, parameters

  def sync(self, config, state):
    # time_extracted = singer.utils.now()
    records, parameters = self.get_records(config)
    singer.write_records(self.report["name"], records)
    self._write_state(state, parameters)

  def _write_state(self, state, parameters):
    report_state = state.get(self.report["name"], [])
    state[self.report["name"]] = report_state
    report_state.append({
      "parameters": parameters,
      "timestamp": singer.utils.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    })

    singer.write_state(state)

