import json
import os
import sys


def _check_placeholder(key, value):
    if isinstance(value, str) and value.startswith("/path/to/"):
        print(f"ERROR: '{key}' in config.json is still a placeholder ({value}).")
        print("Please copy config.json.example to config.json and fill in your paths.")
        sys.exit(1)


class ConfigReader:
    def __init__(self, config_file):
        self.config_file = config_file

    def read_config(self):
        if not os.path.exists(self.config_file):
            print(f"ERROR: {self.config_file} not found.")
            print("Please copy config.json.example to config.json and fill in your paths:")
            print("  cp config.json.example config.json")
            sys.exit(1)

        with open(self.config_file, 'r') as file_handle:
            config_data = json.load(file_handle)

        try:
            project_dir = config_data['GRAPH_PROJECT_DIR']
            _check_placeholder('GRAPH_PROJECT_DIR', project_dir)
            config_data['GRAPH_PROJECT_DIR'] = project_dir
            print(
                f"Using GRAPH_PROJECT_DIR as set - {config_data['GRAPH_PROJECT_DIR']}")
        except KeyError:
            print("Please set GRAPH_PROJECT_DIR as the path to the FlexoGraph repo in config.json.")
            exit(1)

        try:
            db_dir = config_data['DB_DIR']
            _check_placeholder('DB_DIR', db_dir)
            config_data['DB_DIR'] = db_dir
            print(f"Using DB_DIR as set - {config_data['DB_DIR']}")
        except KeyError:
            print(
                "Please set DB_DIR in config.json")
            exit(1)

        try:
            kron_gen_name = config_data['KRON_GEN_PATH']
            _check_placeholder('KRON_GEN_PATH', kron_gen_name)
            config_data['KRON_GEN_PATH'] = kron_gen_name
            if "PaRMAT" in kron_gen_name:
                print("Using PaRMAT as the Kronecker generator")
            elif "smooth_kron" in kron_gen_name:
                print("Using KronGen as the Kronecker generator")
            elif "gapbs" in kron_gen_name:
                print("Using GAPBS as the Kronecker generator")
            else:
                print(
                    "Please set KRON_GEN_PATH in config.json.")
                exit(1)
        except KeyError:
            print(
                "Please set KRON_GEN_PATH in config.json.")
            exit(1)

        try:
            kron_graphs_path = config_data['KRON_GRAPHS_PATH']
            _check_placeholder('KRON_GRAPHS_PATH', kron_graphs_path)
            print(f"Using KRON_GRAPHS_PATH as set - {kron_graphs_path}")
        except KeyError:
            print(
                "Please set KRON_GRAPHS_PATH in config.json.")
            exit(1)

        try:
            log_dir = config_data['LOG_DIR']
            _check_placeholder('LOG_DIR', log_dir)
        except KeyError:
            print("no log directory found. will default to CWD")
            config_data['log_dir'] = os.getcwd()

        config_data['PROFILE_PATH'] = os.path.join(
            project_dir, "build", "profile")
        config_data['DEBUG_PATH'] = os.path.join(
            project_dir, "build", "debug")
        config_data['RELEASE_PATH'] = os.path.join(
            project_dir, "build", "release")
        config_data['STATS_PATH'] = os.path.join(
            project_dir, "build", "wt_stats")
        config_data['OUTPUT_PATH'] = os.path.join(project_dir, "outputs")
        return config_data


class GraphDatasetReader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = None

    def read_config(self):
        config_data = {}
        with open(self.config_file, 'r') as file_handle:
            config_data = json.load(file_handle)

        config_ok = True
        for dataset in config_data:
            try:
                assert (os.path.exists(dataset['graph_path']))
            except AssertionError:
                print(
                    f"Graph file {dataset['graph_path']} not found. Please check the path.")
                config_ok = False
            except KeyError:
                print(f"Missing keys; Please check the config file.")
                config_ok = False

            try:
                dataset['num_nodes'] = int(dataset['num_nodes'])
                assert (dataset['num_nodes'] > 0)
            except KeyError:
                print(
                    f"Missing num_nodes for {dataset['dataset_name']}; Please check the config file.")
                config_ok = False
            except AssertionError:
                print(
                    f"Error while parsing {dataset['dataset_name']} : num_nodes must be a positive integer")
                config_ok = False

            try:
                dataset['num_edges'] = int(dataset['num_edges'])
                assert (dataset['num_edges'] > 0)
            except KeyError:
                print(
                    f"Missing num_edges for {dataset['dataset_name']}; Please check the config file.")
                config_ok = False
            except AssertionError:
                print(
                    f"Error while parsing {dataset['dataset_name']} : num_edges must be a positive integer")
                config_ok = False
        if (not config_ok):
            exit(1)
        else:
            return config_data
