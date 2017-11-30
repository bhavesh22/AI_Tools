class CatsController < ApplicationController
	protect_from_forgery with: :null_session
	def index
	end

	def predict
		# Cat identification number
		cin = Time.now.strftime('%s')+rand(100).to_s+ "_"
		uploaded_io = params[:picture]
		cat_file_name = cin + uploaded_io.original_filename
		File.open(Rails.root.join('public', cat_file_name), 'wb') do |file|
			file.write(uploaded_io.read) 
		end
		learning_rate = params[:learning_rate].present? ? params[:learning_rate] : 0.001
		num_iteration = params[:num_iteration].present? ? params[:num_iteration] : 100
		print_every = params[:print_every].present? ? params[:print_every] : 2
		variable_learning_rate = params[:variable_learning_rate].present? ? params[:variable_learning_rate] : 1
		binding.remote_pry
		system_command = "python " + "python_scripts/LR1.py " + learning_rate.to_s + " " + num_iteration.to_s + " "+ print_every.to_s + " " + variable_learning_rate.to_s + " " + cin.to_s + " " + cat_file_name
		system system_command
		@cat_identification = ""
		File.open(cin +".txt", "r") do |f|
  		f.each_line do |line|
    		@cat_identification += line
  		end
		end
		@cin = cin
		File.delete(cin +".txt")
		respond_to do |format|
      format.js
    end
	end

	def delete_files
		cin = params[:cin]
		# File.delete('app/assets/images/' + cin +".png")
	end

end
