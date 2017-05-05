# Deploy Server CI Recipe

The goal of this recipe is to provide you with a formula you can use within 
your Jenkins CI environment to add and configure newly provisioned servers to 
your KEMP LoadMaster. This recipie contains two components:

## deploy_server.groovy

This is a [Jenkinsfile pipeline][1] definition. It expects parameterized 
input of the variable `rs` which specifies the new server IP address. This 
pipeline is separated out into stages:


### Installing dependencies

This stage sets up a virtual environment and installs the KEMP API package.


### Add RS to VS

This stage adds the specified new server (real server) to the virtual service 
stored in the script. For a more generalized approach, these values could be 
passed in from the CI job as parameterized variables.


### Drip traffic to new RS

This stage enables the new real server and applies a given percentage of 
overall traffic to the new server. This percentage is stored `drip` variable 
in the pipeline and can be easily changed to become parameterized. 


### Monitor new RS

This stage monitors the health of the server as reported by the LoadMaster. 
It is assumed that the virtual service healthcheck parameters are correctly
set and will return a failed healthcheck in the event of a server problem. 
The value of `status` is set to `1` if the new server fails during this 
period. The duration of the monitoring is stored `monitor_duration` variable 
in the pipeline and can be easily changed to become parameterized.


### Send notification

This stage sends a notification. The notification can be customized as desired 
using any Jenkins plugins, such as email or Slack. The notification can be 
dependant on whether the test was successful. If the test was not successful 
an error is raised at this point to prevent deployment.


### Wait for approval

This stage waits for user approval before giving the new server more traffic. 
This plugin can be customized to limit which users are allowed to approve the 
deployment.


### Deploy to production

This stage "deploys" the server to production by equalizing the weights of all 
the available real servers in the pool. This behavior can be customized 
further to give the new server a different percentage, a fixed weight or other 
behaviors given your particular deployment needs.


## deploy_server.py

This is a Python script which leverages the python-kemptech-api to control a
given LoadMaster and virtual service. It is assumed that the virtual service 
is already created and configured on the LoadMaster. If needed, the LoadMaster 
and virtual service information could be passed in from pipeline to make the 
job more flexible.

There are additional unused actions for `disable` and `remove` which could 
be used in the event of a failure to remove the new server from usage.


## Usage

To use this recipe, first create a repository and add the files in this 
directory, then fill out the variables in the `deploy_server.py` header. 

Next create a Jenkins pipeline job. 
![Create Pipeline][create_pipeline]

Make the project parameterized and add a `String Parameter` named `rs`.
![Add Parameter][add_parameter]

In the `Pipeline` configuration section, select `Pipeline script from SCM` 
and configure it for the SCM repository you created. Specify 
`deploy_server.groovy` as the script path. Be sure to uncheck `Lightweight 
checkout`
![Configure SCM][config_scm]

You should them be able to run the pipeline. Make sure your Jenkins server 
can reach the LoadMaster you specified in the configuration and that the 
virtual service specified exists.

You can then run the pipeline and see the results. If you have the BlueOcean 
plugin installed, you will see the following results:

### Pass
![Pass][pass]

### Fail
![Fail][fail]


[1]: https://jenkins.io/doc/book/pipeline/jenkinsfile/
[create_pipeline]: ./img/create_pipeline.png
[add_parameter]: ./img/add_parameter.png
[config_scm]: ./img/config_scm.png
[pass]: ./img/pass.png
[fail]: ./img/fail.png