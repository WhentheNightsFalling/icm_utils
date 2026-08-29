database_path, run_id = ARGV.last(2)

db = WSApplication.open database_path
run = db.model_object_from_type_and_id('Run', run_id.to_i)

run.children.each do |sim|
  sim.run
  puts "#{sim.id}|#{run.name}|#{sim.name}|#{sim.path}|#{sim.status}"
end