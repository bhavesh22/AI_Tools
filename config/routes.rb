Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  
root 'cats#index'
get '/AI', to: 'cats#index' 
post '/predict', to: 'cats#predict'
post '/delete_files', to: 'cats#delete_files'
end
