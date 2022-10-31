import yaml
from data_val_2022 import DataValidation2022

validation_by_year = {2022: DataValidation2022}
path_to_config = "config.yaml"

with open(path_to_config) as file:
    data_val = validation_by_year[yaml.safe_load(file)["year"]](path_to_config)

data_val.validate_data()
