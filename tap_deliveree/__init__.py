import singer 
from singer.catalog import Catalog, write_catalog
from .report_stream import ReportStream

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = ["base_url", "resource", "reports", "api_key"]

def discover(reports):
  LOGGER.info("Discovery start")
  catalog_entries = []
  for report in reports:
    report_stream = ReportStream(report)
    catalog_entries.append(report_stream.generate_catalog_entry())
  catalog = Catalog(catalog_entries)
  write_catalog(catalog)
  LOGGER.info("Discovery complete")

def generate_catalog(reports):
  catalog_entries = []
  for report in reports:
    report_stream = ReportStream(report)
    catalog_entries.append(report_stream.generate_catalog_entry())
  return Catalog(catalog_entries)

def get_report_stream(reports, tap_stream_id):
  report = next((report for report in reports if report["name"] == tap_stream_id), None)
  if report is None:
    return None
  return ReportStream(report)


def sync(config, state, catalog):
  LOGGER.info("Sync start")
  selected_streams = catalog.get_selected_streams(state)
  reports = config["reports"]
  for stream in selected_streams:
    report_stream = get_report_stream(reports, stream.tap_stream_id)
    if report_stream is None:
      LOGGER.error(f"Report not found: {stream.tap_stream_id}")
      continue
    report_stream.write_schema()
    report_stream.sync(config, state)
  LOGGER.info("Sync complete")

def main():
    args = singer.utils.parse_args(required_config_keys=REQUIRED_CONFIG_KEYS)
    config = args.config
    reports = config["reports"]

    if args.discover:
      discover(reports)
    else:
      if args.catalog:
        catalog = args.catalog
      else:
        catalog = generate_catalog(reports)
      sync(config, args.state, catalog)

if __name__ == "__main__":
    main()