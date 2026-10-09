

import icm_utils
from icm_utils import Simulation

config = icm_utils.ICMConfig(exchange_path="C:\\Program Files\\Autodesk\\InfoWorks ICM Ultimate 2026\\ICMExchange.exe")

testing_session = icm_utils.ICMSession(config=config, database_path="C:\\Users\\micha\\Desktop\\Infoworks ICM Testing database\\test_database.icmm")

simlist = testing_session.list_simulations()

for sim in simlist:
    print(sim.id)
