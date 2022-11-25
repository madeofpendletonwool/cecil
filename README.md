<h1 align='center'> Cecil <h1> 
<h2 align='center'> A Python based Notification stack <h2> 

### Welcome to Cecil

Cecil is an ever growing notification platform that can be used for all notification needs. It pairs perfectly with [ntfy](https://ntfy.sh/) - A fantastic program built to send and handle notifications at zero cost - and will assume you're using it throughout these instructions. You're welcome to implement your own notification service but you assume the upkeep with it. 

The intention of this program is to very generically handle any kind of reporting you need. My goal is to keep it very simple, but also provide whatever type of 'module' that might be needed. This is why the code is broken into individual folders. You can utilize only what you need, and it's easy to make adjustments. 

### Deployment

Deployment of any modules is a piece of cake.

First in the environment you want to run any modules in just run the setup.sh script. This will copy the cecil files over to a folder in /opt called 'cecil'. All files will be in there from here on out. It also installs any dependancies that are needed for any modules using pip. From there, follow instructions on any individual module in the documentation below. One thing I will say is that it's pretty handy to set up the running of any of these modules using some sort of CI/CD/automation software. I use github actions. First I deploy cecil using an actions workflow. Create a workflow that pulls the cecil repo and then runs the setup.sh script on all servers you want to run cecil on. From there you just need to run the ansible playbooks on scripted intervals. The docs on each module will go into more details on the playbooks. 

### Docker Monitor
Docs Coming soon!

### Linux Health
Docs Coming Soon!