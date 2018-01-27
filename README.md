# Building a Dictionary Bot for Facebook Messenger on Hasura

This tutorial is a guide to run a **Dictionary bot on facebook messenger**, that fetches meaning/definition of the user search terms/inputs, in real time, using [PyDictionary](https://pypi.python.org/pypi/PyDictionary) module.

![fb-bot-2018-01-28_00 10 26](https://user-images.githubusercontent.com/20622980/35475199-475656c2-03c0-11e8-8882-07b31b5cd174.gif)

For the chat bot to function we'll need a server that will receive the messages sent by the Facebook users, process this message and respond back to the user. To send messages back to the server we will use the graph API provided by Facebook. For the Facebook servers to talk to our server, the endpoint URL of our server should be accessible to the Facebook server and should use a secure HTTPS URL. For this reason, running our server locally will not work and instead we need to host our server online. In this tutorial, we are going to deploy our server on Hasura which automatically provides SSL-enabled domains.

You can get the full code for the project from this [Github repository](https://github.com/vishalpolley/fb-dictionary-bot).


## Pre-requisites

- [Hasura CLI](https://docs.hasura.io/0.15/manual/install-hasura-cli.html)

- [Git](https://git-scm.com)

- [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/) (required only for local development)

- [Flask](http://flask.pocoo.org/)


## Getting the bot running

### Create a facebook application

* Navigate to https://developers.facebook.com/apps/

* Click on **'+ Create a new app’** or **'+ Add a new app’**.


![fb app photo1](https://user-images.githubusercontent.com/20622980/35475394-e0a6651c-03c3-11e8-894e-e23f1c5773d5.png)


* Give a **Display Name** for your app and your **Contact Email**.


![fb app photo2](https://user-images.githubusercontent.com/20622980/35474339-ef8a9e6a-03b2-11e8-8ac1-5fcfad27a88d.png)


* In the select a product screen, hover over **Messenger** and click on **Set Up**


![fb app photo3](https://user-images.githubusercontent.com/20622980/35475404-0dca5f80-03c4-11e8-8069-b41626ef9e77.png)


* To start using the bot, we need a facebook page to host our bot.

  + Scroll over to the **Token Generation** section

  + Choose a page from the dropdown (Incase you do not have a page, create one [here](https://www.facebook.com/pages/create))

  + Once you have selected a page, a *Page Access Token* will be generated for you.

  + Save this token somewhere.


![Page Token](https://user-images.githubusercontent.com/20622980/35475423-37019c88-03c4-11e8-9fa3-38d62f2dd5ad.png)


* Now, we need to trigger the facebook app to start sending us messages

  - Switch back to the terminal

  - Paste the following command:

```sh
# Replace <PAGE_ACCESS_TOKEN> with the page access token you just generated.
$ curl -X POST "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=<PAGE_ACCESS_TOKEN>"
```

* In this project, we are using [PyDictionary](https://pypi.python.org/pypi/PyDictionary) python module to get the meaning/definition of the input term/word in real time. 

### Getting the Hasura project

```
$ hasura quickstart vishalpolley/fb-dictionary-bot
$ cd fb-dictionary-bot
# Add FACEBOOK_VERIFY_TOKEN to secrets. This is any pass phrase that you decide on, keep a note on what you are choosing as your verify token, we will be using it later while setting things up for your bot on the facebook developer page.
$ hasura secrets update verify.token <YOUR-VERIFY-TOKEN>
# Add FACEBOOK_PAGE_ACCESS_TOKEN to secrets
$ hasura secrets update page.access.token <YOUR-FB-PAGE-ACCESS-TOKEN>
# Deploy
$ git add . && git commit -m "Deployment commit"
$ git push hasura master
```

After the `git push` completes:

```sh
$ hasura microservice list
```

You will get an output like so:

```sh
INFO Getting microservices...                     
INFO Hasura microservices:                        
USER MS NAME     STATUS      INTERNAL-URL       EXTERNAL-URL          
app              Running     app.default:80     http://app.debriefing13.hasura-app.io/

HASURA MS NAME     STATUS      INTERNAL-URL                  EXTERNAL-URL
le-agent           Running                                   
session-redis      Running     session-redis.hasura:6379     
sshd               Running                                   
platform-sync      Running                                   
gateway            Running                                   
data               Running     data.hasura:80                http://data.debriefing13.hasura-app.io/
filestore          Running     filestore.hasura:80           http://filestore.debriefing13.hasura-app.io/
notify             Running     notify.hasura:80              http://notify.debriefing13.hasura-app.io/
postgres           Running     postgres.hasura:5432          
auth               Running     auth.hasura:80                http://auth.debriefing13.hasura-app.io/
```

Find the EXTERNAL-URL for the service named `bot` and keep a note of it after changing the `http` to `https` in the URL. 
(For example, in this case -> http://app.debriefing13.hasura-app.io/).

### Enabling webhooks

In your fb app page, scroll down until you find a card name `Webhooks`. Click on the `setup webhooks` button.

![Enable Webhooks](https://user-images.githubusercontent.com/20622980/35474409-e5c7ee0e-03b3-11e8-8046-0345c2f23854.png)

* The `callback URL` is the URL that the facebook servers will hit to verify as well as forward the messages sent to our bot. The flask app in this project uses the `/webhook` path as the `callback URL`. Making the `callback URL` https://bot.YOUR-CLUSTER-NAME.hasura-app.io/webhook (in this case -> https://app.debriefing13.hasura-app.io/webhook/)

* The `verify token`is the verify token that you set in your secrets above (in the command `$ hasura secrets update verify.token <YOUR-VERIFY-TOKEN>`)

* After selecting all the `Subsciption Fields`. Submit and save.

* You will also see another section under `Webhooks` that says `Select a page to subscribe your webhook to the page events`, ensure that you select the respective facebook page here.

Next, open up your facebook page.

* Hover over the **Send Message** button and click on Test Button.


![Test Button](https://user-images.githubusercontent.com/20622980/35475378-97e242a6-03c3-11e8-82d6-9ddf9159fa65.png)


* Instead, if your button says **+ Add Button**, click on it.

* Next, click on **Use our messenger bot**. Then, **Get Started** and finally **Add Button**.

* You will now see that the **+ Add button** has now changed to **Get Started**. Hovering over this will show you a list with an item named **Test this button**. Click on it to start chatting with your bot.

* Send a message to your bot.

Test out your bot. On receiving a word, it should reply back with the meaning of the word.

**Here is the bot in action**

![fb-bot-2018-01-28_00 10 26](https://user-images.githubusercontent.com/20622980/35475199-475656c2-03c0-11e8-8882-07b31b5cd174.gif)

## Support

If you happen to get stuck anywhere, feel free to raise an issue [here](https://github.com/vishalpolley/fb-dictionary-bot/issues)

Also, you can contact me via [email](mailto:vishalpolley290996@gmail.com) or [linkedin](https://www.linkedin.com/in/vishalpolley/) or [facebook](https://www.fb.com/vishal.polley).
