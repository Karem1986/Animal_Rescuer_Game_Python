# Goal of this app

The goal of this app is to show Python skills with the Flask frontend web framework deployed to Render cloud server.

The project lives at: <https://animal-rescuer-game-python.onrender.com>

As a cloud service, Render was the choice since it makes easy to run Docker containerized applications. One thing to note is that in Render the recommended server is gunicorn which is defined in the
Dockerfile like this:

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.index:app"]

This This tells Docker: “Run Gunicorn, bind to port 8080, and serve the app object from app/index.py.”

And then in your Render dashboard project settings change the "start command" to:

gunicorn app.index:app

More information about deployment in Render: <https://render.com/docs/deploys#deploy-steps>

## Flask web based application

The flask app file is configured to run as a Flask web app in the browser (See Dockerfile)

    docker build -t karin86/pythonapp:latest .
    docker run -p 8080:5000 -p 8000:8000 karin86/pythonapp:latest
    ![See the game!](Game.png)

Access via localhost:8080 (See Dockerfile)

## Adding new changes/extending the application

If adding any changes to the application, dockerfile execute the following commands afterwards:

- Rebuild and push the image to docker hub registry:
    docker build -t karin86/pythonapp:latest .
    docker push karin86/pythonapp:latest
- Then force Kubernetes to pull this image from the registry:
    kubectl rollout restart deployment rescue-app -n testingopentelemetry
- Confirm that the pod has been restarted:
    kubectl get pods -n testingopentelemetry
- Check the memory crash:
    kubectl describe pod pod-name -n testingopentelemetry

You should see something similar to this under the Container section:

    State:          Waiting
    Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
      Started:      Tue, 01 Apr 2025 11:07:30 +0200
      Finished:     Tue, 01 Apr 2025 11:07:42 +0200
    Ready:          False
    Restart Count:  4
