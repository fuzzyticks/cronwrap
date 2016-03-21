#Cronjob Scheduling and Performance Analysis
-------------------------------------------

Handling cronjobs become tedious task as number of hosts and crons increases. Possibility of human error arise while adding/removing cronjobs. For adding and removing one has to ssh to the hosts or run some remote execution script based on ssh to set cronjobs on the host, which is not easy to tackle.

Also there is no easy way to check cronjob resource utilization, for example cronjob cpu usage, memory usage, page_faults, exit_status, start/end time, total time took to execute the job, etc. No metrics available with respect to crons on various hosts, System admins hardly able capture performance of crons unless something alerts on monitoring system or unless they are already present on the host running the cron, During odd hours this job become more tedious and difficult to do. Developers also have no way to analyze the performance of their cron scripts.`

System is designed over existing known and free and open source technologies, like Linux, Saltstack, Elasticseach, Python flask, HTML, CSS, JavaScript ..

Scope -:

- Simple web interface to Add / Remove / Search and Analyse crons scheduled on multiple hosts, using an existing saltstack infrastructure.
- To capture all performance metrics for any cronjob on all hosts. Metrics like start time, end time, cpu usage, mem usage, page faults, exit status by crons.
- Data analysis based on user, time taken, start/end time, hosts, exit status, cpu usage, memory usage, page faults and hostname.

Software used -:

- Any Linux distribution having linux kernel version >=2.6
- GNU time 1.7 [For gathering the performance metrics of a job]
- Crond as scheduler service or Any similar cron service.
- Python 2.7 [cronjob wrapper script]
- Flask 0.10 [For handling http request / response cycle and serving static pages]
- Elasticsearch >=2.0 [for storing metrics gatherd using GNU time]
- Saltstack >=  2015.8.5 [For remote execution framework]
- Jquery, Bootstrap [WebPages are designed using HTML, Jquery and Twitter bootstrap]

Assumptions -:

- Assuming cronjob scripts/commands required to be executed by crond are present already on host. This system will not help in distributing the executable files to hosts.
- Cronwrap metric collection script required to be present on linux at /usr/bin/cronwrap and must be executable, So it should be transferred to all hosts during initial setup of system.
- GNU /usr/bin/time must be present on all the hosts. This will help in capturing metric of cronjob. Cronwrap script depends on this tool.
- Infrastructure must be running with Saltstack, Master / Minion must be configured properly. As this system relies on saltstack for remote execution, for adding and removing crons. Setting up staltstack is out of scope of this project work.
- Application is required to be deploy on same host as salt master, as system uses salt master client api's which requires app to be on same host for authentication (using client_cli authentication. Salt do provide various external auth api's also).

	Snippet of Salt Master config (here cronwrapuser is a system user).
	client_acl:
	   cronwrapuser:
	     - test.ping
	     - test.fib
	     - cmd.run
	     - cmd.has_exec
	     - cron.*

Note -: System is not complete, and not at all safe for any running environment yet, It is just an attempt to provide a working model, It can be improved further and more things can be incorporate easily (Like developing recommendation service, which can suggest time slots for running a job based on collected data in elastic, we can visualize metrics using kibana or other tools, wrapper script can freely be used for capturing any job/command (either executing through crond or directly by user) etc etc....
