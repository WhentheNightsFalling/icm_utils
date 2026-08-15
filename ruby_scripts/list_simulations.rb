#IExchange puts arguements into ARGV, ARGv[-1] ensures it gets the last argument, which is the database path
db = WSApplication.open ARGV[-1]
 
sims = db.model_object_collection('Sim')
 
sims.each do |sim|
  run = db.model_object_from_type_and_id(sim.parent_type, sim.parent_id)
  puts "#{sim.id}|#{run.name}|#{sim.name}|#{sim.path}|#{sim.status}"
end
 