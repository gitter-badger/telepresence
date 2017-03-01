## Theory of operation

A Kubernetes production environment looks like this:

<div class="mermaid">
graph TD
  subgraph Kubernetes
    code[Your code]
    s1[Your service]-->code
    code-->s2[Service 2]
    code-->s3[Service 3]
  end
  subgraph Cloud
    code-->c1[Cloud Database]
  end
</div>

Currently Telepresence works by running your code locally in a Docker container, and forwarding requests to/from the remote Kubernetes cluster.

<div class="mermaid">
graph TD
  subgraph Laptop
    code[Your code, in container]
  end
  subgraph Kubernetes
    code-.-proxy[Telepresence proxy]
    s1[Your service]-->proxy
    proxy-->s2[Service 2]
    proxy-->s3[Service 3]
  end
  subgraph Cloud
    proxy-->c1[Cloud Database]
  end
</div>

(Future versions may allow you to run your code locally directly, without a local container.
[Let us know](https://github.com/datawire/telepresence/issues/1) if this a feature you want.)

## How to use Telepresence

Let's assume you have a web service which listens on port 8080, and has a Dockerfile which gets built to an image called `examplecom/yourservice`.

Your Kubernetes configuration will typically have a `Service`:

```yaml

```

You will also have a `Deployment` that actually runs your code:

```yaml
```

In order to run Telepresence you will need to do three things:

1. Replace your production `Deployment` with a custom `Deployment` that runs the Telepresence proxy.
2. Run the Telepresence client locally in Docker.
3. Run your own code in its own Docker container, hooked up to the Telepresence client.

Let's go through these steps one by one.

### 1. Run the Telepresence proxy in Kubernetes

### 2. Run the local Telepresence client on your machine

### 3. Run your code locally in a container

### 4. Better local development with Docker

To make Telepresence even more useful, you might want to use a custom Dockerfile setup that allows for code changes to be reflected immediately upon editing.

For interpreted languages the typical way to do this is to mount your source code as a Docker volume, and use your web framework's ability to reload code for each request.
Here are some tutorials for various languages and frameworks:

* [Python with Flask](http://matthewminer.com/2015/01/25/docker-dev-environment-for-web-app.html)
* [Node](http://fostertheweb.com/2016/02/nodemon-inside-docker-container/)

## Help us improve Telepresence!

We are considering various improvements to Telepresence, including:

* [Removing need for Kubernetes credentials](https://github.com/datawire/telepresence/issues/2)
* [Allowing running code locally without a container](https://github.com/datawire/telepresence/issues/1)

Please add comments to these tickets if you are interested in these features, and [file a new issue](https://github.com/datawire/telepresence/issues/new) if you find any bugs or have any feature requests.

## Alternatives

Some alternatives to Telepresence:

* Minikube is a tool that lets you run a Kubernetes cluster locally.
  You won't have access to cloud resources, however, and your development cycle won't be as fast since access to local source code is harder.
  Finally, spinning up your full system may not be realistic if it's big enough.
* Docker Compose lets you spin up local containers, but won't match your production Kubernetes cluster.
  It also won't help you access cloud resources, you will need to emulate them.
* Pushing your code to the remote Kubernetes cluster.
  This is a somewhat slow process, and you won't be able to do the quick debug cycle you get from running code locally.