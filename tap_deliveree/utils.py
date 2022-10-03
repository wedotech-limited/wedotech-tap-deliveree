from datetime import datetime, timedelta

PARAMETER_PARSERS = {
  "CURRENT_DATE": lambda v: datetime.now().strftime("%Y-%m-%d"),
  "PREVIOUS_DATE": lambda v: (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
  "CURRENT_TIMESTAMP": lambda v: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  "PREVIOUS_TIMESTAMP": lambda v: (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
}

def parse_parameter_value(value):
    """
    Parse the parameter value and return the parsed value
    """
    if value in PARAMETER_PARSERS:
        return PARAMETER_PARSERS[value](value)
    return value

def parse_parameters(parameters: dict):
    """
    Parse the parameters from the config and return a dictionary of parameters
    """
    params = {}
    for param, value in parameters.items():
        params[param] = parse_parameter_value(value)
    return params