import base64
from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import tempfile
import pandas as pd

@dataclass
class ICMConfig:
    """Configuration class for Infoworks ICM. This holds the properties of the installation."""
    exchange_path:Path #"C:\Program Files\Autodesk\InfoWorks ICM Ultimate 2026\ICMExchange.exe"
    product: str = "ICM"
    timeout_s: int = 300

@dataclass
class Simulation:
    id: str
    run_name: str
    sim_name: str
    path: str
    status: str

class ScriptLibrary:
    """A library for locating Ruby scripts to be run by Exchange."""
    def __init__(self):
        self.script_dir = Path(__file__).parent / "ruby_scripts"
        
    def get_script_path(self, script_name:str)->Path:
        # Locates ruby scripts to be run by Exchange
        return self.script_dir / f"{script_name}.rb"

class ExchangeRunner:
    """A runner for executing Ruby scripts via Exchange."""
    def __init__(self, config:ICMConfig):
        self.config = config

    def run_script(self, script_path:Path, args=None):
        # Runs a Ruby script via Exchange with the given arguments where required, this is database agnostic and can be used for any ICM session
        if args is None:
            args = []
        return subprocess.run([self.config.exchange_path, script_path, self.config.product,*args],capture_output=True,text=True)
        

class ICMSession:
    """Public facing class for interacting with Infoworks ICM."""

    def __init__(self, config:ICMConfig,database_path:str):
        self.config = config
        self.database_path = database_path
        self.exchange_runner = ExchangeRunner(config)
        self.scripts = ScriptLibrary()

    def _pack_options(self,**kwargs) -> str:
        # Packs the options lists into a base64 encoded JSON string for passing to the Ruby script, if this isn't done the quotation marks won't be parsed by ruby
        options_json = base64.b64encode(json.dumps(kwargs).encode('utf-8')).decode('ascii')
        return options_json

    def list_simulations(self):
        # Lists all simulations in the database
        args =[self.database_path]
        list_of_sims_output=[]
        script_path = self.scripts.get_script_path("list_simulations")
        ruby_output=self.exchange_runner.run_script(script_path, args)
        for line in ruby_output.stdout.splitlines():
            parts = line.split('|')
            sim = Simulation(id=parts[0], run_name=parts[1], sim_name=parts[2], path=parts[3], status=parts[4])
            list_of_sims_output.append(sim)
        return list_of_sims_output

    def sims_to_dict(self):
        # Returns a dictionary of simulations in the database, with keys as "run_name_sim_name" and values as Simulation objects
        sim_dict = {}
        sim_list = self.list_simulations()
        keys=[]
        for sim in sim_list:
            key = (sim.run_name+"_"+sim.sim_name)
            keys.append(key)

        for i in range(0,len(keys)):
            if keys.count(keys[i])>1:
                    keys[i]=keys[i]+"_"+str(keys.count(keys[i]))

        for i in range(0,len(sim_list)):
            sim_dict[keys[i]] = sim_list[i]

        return sim_dict

    def run_simulation(self, sim:Simulation):
        #Runs the simulation using the most up to date network
        pass # Placeholder for future implementation

    def extract_simulation_results(self, sim:Simulation,selection=None,attributes=None):
        #Extracts simulation results for one element type with multiple compatible attributes, returns a dataframe
        results=self.batch_extract_simulation_results(sim=sim,selection=selection,attributes=attributes)
        if len(results) != 1:
            raise ValueError(f"Expected exactly one table, got {len(results)}: {list(results.keys())}. Use batch_extract_simulation_results for multiple tables.")
        results_df=results[list(results.keys())[0]]
        return results_df

    def batch_extract_simulation_results(self, sim:Simulation,selection=None,attributes=None):
        #Extracts simulation results for multiple element types with multiple attributes, returns a dictionary of dataframes
        results_dict = {}

        temp=tempfile.mkdtemp()

        json_options = self._pack_options(selection=selection,attributes=attributes)
        args=[self.database_path, temp, sim.id, json_options]
        script_path = self.scripts.get_script_path("extract_simulation_results")
        self.exchange_runner.run_script(script_path, args)
        for file in Path(temp).glob("*.csv"):
            results_dict[file.stem] = pd.read_csv(file)
        return results_dict

    def list_networks(self):
        #lists all networks in the database, returns a list of network names
        pass # Placeholder for future implementation

    def extract_network_data(self,element_type:str):
        #Extracts network data for a given element type, returns a dictionary of dataframes
        pass # Placeholder for future implementation

    def commit_network_changes(self,changes:dict):
        #Commits network changes to the database, changes should be a dictionary of dataframes with keys as element types and values as dataframes with the changes
        pass # Placeholder for future implementation


"""To-do:
    ICM Modeling Core:
        Add methods for:
            Retrieving simulation results
                Specifying element
                Specifying specific results (e.g. flow, depth, velocity)
             Setting up and running simulations
                Specifying simulation parameters
                Running simulations
            Listing networks
                Scenario listing and switching
            Retrieving network elements:
                Nodes
                Links
                Subcatchments
            Editing network elements:
                Nodes
                Links
                Subcatchments
    Model Calibration Toolkit:
        Add methods for:
            Observed vs. Simulated comparison
                Peak flows
                Flow volumes
                Time to peak
            Event Identification
                Simple thresholding with a user-defined threshold and interevent time
    """
