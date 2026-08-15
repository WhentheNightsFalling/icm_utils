

import icm_results
from icm_results import Simulation

config = icm_results.ICMConfig(exchange_path="C:\\Program Files\\Autodesk\\InfoWorks ICM Ultimate 2026\\ICMExchange.exe")

testing_session = icm_results.ICMSession(config=config, database_path="C:\\Users\\micha\\Desktop\\Infoworks ICM Testing database\\test_database.icmm")

simlist = testing_session.list_simulations()

result=testing_session.extract_simulation_results(sim=simlist[0],attributes=[["link", ["us_depth"]]])
print(result)