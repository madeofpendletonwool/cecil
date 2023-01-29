<h1 align='center'> Cecil <h1>
<h2 align='center'> A Python based Notification stack with a Flutter Web UI <h2> 
<p align="center">
<img src="./images/Cecil-logos.jpeg">
</p>

## Welcome to Cecil

Cecil is an ever growing notification platform that can be used for all notification needs (with the right modules implemented). It pairs perfectly with [ntfy](https://ntfy.sh/) - A fantastic program built to send and handle notifications at zero cost - and will assume you're using it throughout these instructions. You're welcome to implement your own notification service but you assume the upkeep with it. 

The intention of this program is to very generically handle any kind of reporting you need. My goal is to keep it very simple, but also provide whatever type of 'module' that might be needed. This is why the code is broken into individual folders. You can utilize only what you need, and it's easy to make adjustments. 

It also requires next to zero knowledge of Python or Flutter (or Flet, the python based Flutter wrapper that this program is built on) to setup modules yourself. It comes with an easy to use and intuitive web ui that has help dropdowns throughout to assist you. 

### Setup and Deployment

Deployment of any modules is a piece of cake.

Cecil is containerized and can be easily deployed with a docker-compose file. This is my recommended way to set it up as you can very easily assign the required variables for authentication. The official docker image is located here:
https://hub.docker.com/r/madeofpendletonwool/cecil
Here's an example docker compose file 

```
version: '3'
services:
  cecil:
    image: madeofpendletonwool/cecil:latest
    container_name: cecil
    tty: true
    environment:
      # ID and Secret for Github Authentication
      - CLIENT_ID={{ Github_ClientID }}
      - CLIENT_SECRET={{ Github_Secret }}
      # The auth URL is the url that you are using to connect to the app. This is required so the auth token is directed to the right location. Use the url that you use for cecil plus '/api/oauth/redirect' at the end. 
      - AUTH_URL="http://localhost:38355/api/oauth/redirect"
    ports:
      - 38355:38355
    volumes:
      - ~/cecil/config:/opt/cecil
    restart: always
```

The CLIENT_ID, CLIENT_SECRET, and AUTH_URL can be gained by walking through the authentication step below. Feel free to work through that first and then come back here.

Notice port 38355 is being exposed. This is the port that cecil uses inside the container to run the flutter web ui on. Feel free to change the external facing port if you'd like to assign something else. 

Also take note of the mapped volume. Upon creation Cecil will dump all the modules, data and configuration to the mapped config folder. I recommend creating a config folder in a folder called cecil under your user home but you're welcome to use whatever folder you'd like instead if you have a preference. Just assign 755 permission to the entire folder as cecil will need to write to this folder not only during container creating but cecil often creates temp files that it removes as tasks occur with modules. 
```
mkdir -p ~/cecil/config
chmod -R 755 ~/cecil/config
```
I also recommend putting the compose file right in the cecil folder to keep things nicely organzied. But again, use whatever work flow works best for you. 

Once you have all your authentication settings squared away and have the folders created and permissions set, feel free to start things up!
```
sudo docker-compose up
```
You should see the container print out your variables and run a few startup tasks. From there you should be able to open the Cecil application from a web browser.
http://cecil.yourdomain.com:38355
or 
https://cecil.yourdomain.com
^ Whatever domain you choose should be the same as your auth url.

Cecil can easily be put behind a load balencer like nginx or traefik. Make sure to enable websockets support.

### Authentication
Currently, the only Authentication method supported is via Github. Azure Authentication among numerous others will be supported in the future. Github authentication setup is really simple for the time being and organizations and create one single OAuth app to authenticate entire teams with MFA support. 

Here's how to do this:


### Requests
I welcome requests for new modules that would be helpful to you. If a module is helpful for you it's likely to be helpful to others. Please open a feature request by opening an issue with an enhancement label and I will attempt to address it. 

### Todo
- Finish development on Linux Health
- Finish development on Docker monitor
- Finish development on Dell iDrac reports
- File Checker Module
- Show Current static IP on Dynamic IP Scanner
- Implement additional authentication methods
### Development Help
In addition to welcoming requests I also welcome development assistance with any of the modules, feel free to implement new ones and open a pull request for me to merge it in!

## Modules

### Docker Monitor
Docs Coming soon!

### Linux Health
Docs Coming Soon!

### Dynamic IP Updater
Docs Coming Soon!