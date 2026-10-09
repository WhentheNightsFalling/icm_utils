# IExchange prepends its own "ADSK" token to ARGV, so we take the argument from the end
database_path = ARGV.last(1)[0]

db = WSApplication.open database_path

networks = db.model_object_collection('Model Network')

networks.each do |net|
  puts "#{net.id}|#{net.name}|#{net.path}"
end