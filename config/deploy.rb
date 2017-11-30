# Change these
server 'ubuntu@54.200.183.56', port: 22, roles: [:web, :app, :db], primary: true

set :repo_url,        'git@github.com:bhavesh22/AI_Tools.git'
set :application,     'cat_app'
set :user,            'bhavesh22'

# config valid only for current version of Capistrano
# lock "3.8.1"

# Default branch is :master
# ask :branch, proc { `git rev-parse --abbrev-ref HEAD`.chomp }.call

# Default deploy_to directory is /var/www/my_app_name


# Default value for :scm is :git
# set :scm, :git

# Default value for :format is :pretty
# set :format, :pretty

# Default value for :log_level is :debug
# set :log_level, :debug

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# set :linked_files, fetch(:linked_files, []).push('config/database.yml', 'config/secrets.yml',  'config/settings.yml')

# Default value for linked_dirs is []
# set :linked_dirs, fetch(:linked_dirs, []).push('log', 'tmp/pids', 'tmp/cache', 'tmp/sockets', 'vendor/bundle', 'public/system')

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for keep_releases is 5
set :keep_releases, 5

set :passenger_restart_with_touch, true
# namespace :deploy do

#   after :restart, :clear_cache do
#     on roles(:web), in: :groups, limit: 3, wait: 10 do
#       # Here we can do anything such as:
#       # within release_path do
#       #   execute :rake, 'cache:clear'
#       # end
#     end
#   end

#   before :restart, :clear_cache do
#     on roles(:web) do
#       execute "cp #{release_path}/config/settings.yml.#{fetch(:deploy_env)} #{release_path}/config/settings.yml"
#       execute "cp #{release_path}/public/robots.txt.#{fetch(:deploy_env)} #{release_path}/public/robots.txt"
#       execute "cp #{release_path}/config/environments/production.rb.#{fetch(:deploy_env)} #{release_path}/config/environments/production.rb"
#     end
#   end

#   task :delayed_job do
#     if fetch(:delayed_job_status).to_s == "off"
#       invoke 'delayed_job:stop'
#     else
#       invoke 'delayed_job:restart'
#     end
#   end

#   task :inform_slack do
#     puts "=========================== Informing the slack now =============================="
#     uri = URI(URI.encode("https://holachef.slack.com/services/hooks/slackbot?token=eKldKbAmaqYEcGetKc8gbr2f&channel=#deployments"))
#     message = "#{ENV['USERNAME'] || ENV['USER']} deployed #{fetch(:branch)} on #{fetch(:stage)}"
#     Net::HTTP.start(uri.host, uri.port, use_ssl: true, :read_timeout => 10) do |http|
#       http.request_post uri, message
#     end
#   end

# end

# after "deploy:publishing", "deploy:delayed_job"
# after "deploy:publishing", "deploy:inform_slack"
