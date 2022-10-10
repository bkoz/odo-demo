Using vscode with python on Openshift

Install the version 3 [odo client](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/odo/) into a 
directory in your `$PATH`. 

Install the latest [oc client](https://mirror.openshift.com/pub/openshift-v4/x86_64/clients/ocp/latest/) into a 
directory in your `$PATH`. 

From a web browser, login to an Openshift cluster.
In the upper right menu under your name, choose `Copy Login Command -> Display Token` then copy the `server` and `token` arguments from the example `oc` command string.

Create and change to a new directory. Launch vscode and open the folder that you created.
```
mkdir demo
cd demo
```

Launch vscode and open 2 terminals. Launch a web browser and login to
the Openshift web console.

Perform the following steps using the `odo` client from a vscode terminal. 

Login to the Openshift API server.
```
odo login --token=sha256~logintoken --server=https://api.ocp.mysandbox.com:6443
```

Create a new project.
```
odo create project bktest01
```
Example output.
```
 ✓  Project "bktest01" is ready for use
 ✓  New project created and now using project: bktest01
 ```

Create a new python flask application named `flask-example`.
```
odo init --name flask-example --starter=flask-example --devfile=python
```

Start developer mode to allow for local interactive development.
```
odo dev
```
Example output.
```
  __
 /  \__     Developing using the flask-example Devfile
 \__/  \    Namespace: bktest01
 /  \__/    odo version: v3.0.0-rc2
 \__/

↪ Deploying to the cluster in developer mode
 •  Waiting for Kubernetes resources  ...
 ⚠  Pod is Pending
 ✓  Pod is Running
 ✓  Syncing files into the container [891ms]
 ✓  Building your application in container on cluster (command: pip-install-requirements) [3s]
 •  Executing the application (command: run-app)  ...
 -  Forwarding from 127.0.0.1:40001 -> 8080

↪ Dev mode
 Status:
 Watching for changes in the current directory /Users/bkozdemb/demo

 Keyboard Commands:
[Ctrl+c] - Exit and delete resources from the cluster
     [p] - Manually apply local changes to the application on the cluster
Pushing files...

File /Users/bkozdemb/demo/.odo changed
 •  Waiting for Kubernetes resources  ...
 ✓  Syncing files into the container 

↪ Dev mode
 Status:
 Watching for changes in the current directory /Users/bkozdemb/demo

 Keyboard Commands:
[Ctrl+c] - Exit and delete resources from the cluster
     [p] - Manually apply local changes to the application on the cluster
```

The `odo` client should set up a port-forwarding rule that will allow access
to your application endpoint at [http://127.0.0.1:40001](http://127.0.0.1:40001). Even
though the python application is running in Openshift, it can be accessed via a local IP and port.

```
curl http://127.0.0.1:40001

Hello World!
```

In VSCode, edit the `app.py` file and make a simple code change.

Save the file and `odo` will push any changes to the running pod in Openshift. Another curl
command may be used to verify the change.
```
curl http://127.0.0.1:40001

Hello World!
```

### Adding a database

Create a postgresql database using a built-in Openshift template. This may be done via the `oc` CLI or Openshift console.

CLI example
```
oc new-app --template=postgresql-ephemeral -p POSTGRESQL_USER=postgres -p POSTGRESQL_PASSWORD=postgres -p POSTGRESQL_DATABASE=postgres --dry-run=False
```

Replace the contents of `app.py` that was created by the `odo` template with the version in this repo. It contains basic code
to connect to the postgresql database and return the connection IP address. 

Initially, the app will error because the `psycopg` library can't be found. Running `curl` and examining the logs will reveal this.
```
curl 127.0.0.1:40001
```
```
curl: (52) Empty reply from server
```
```
oc logs flask-example-app-<pod-id>
```
```
...
File "/projects/app.py", line 3, in <module>
   import psycopg
ModuleNotFoundError: No module named 'psycopg'
```

Fix this by replacing adding `psycopg[binary]` to the `requirements.txt` file that was created by `odo init`.

We're getting closer. The logs should reveal that the app runs but fails to connect to the database server.
```
oc logs flask-example-app-<pod-id>
```
```
...
INFO:root:POSTGRESQL_DATABASE = None
INFO:root:POSTGRESQL_USER = None
INFO:root:POSTGRESQL_PASSWORD = None
INFO:root:DB Connection Failed!
INFO:root:Exiting.
```

Notice the environment variables needed for authentication are null.

Fixed that by the replacing the contents of `devfile.yaml` that was created by the `odo` template with the version in this repo.

After modifying `devfile.yaml` you should notice that a new pod will get built and deployed. Now the `curl` should suceed.

```
curl 127.0.0.1:40001
```
```
Connected to postgresql at 172.30.224.110
```

Congratulations for orchestrating your first Openshift application!

This concludes the demo.