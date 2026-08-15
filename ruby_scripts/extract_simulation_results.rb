require 'json'
require 'base64'
 
database_path, output_folder, sim_id, options_json = ARGV.last(4)
 
decoded_json = Base64.decode64(options_json)
options = JSON.parse(decoded_json)
selection = options['selection']    # nil (whole network) or a selection list ID/path/name
attributes = options['attributes']  # nil (all attributes) or [["Node", ["depth", ...]], ...]
 
db = WSApplication.open database_path
sim = db.model_object_from_type_and_id('Sim', sim_id.to_i)
 
sim.results_csv_export_ex(selection, attributes, output_folder)
 
# Tell Python exactly which file(s) got created
Dir.glob(File.join(output_folder, '*')).each do |f|
  puts f
end
 