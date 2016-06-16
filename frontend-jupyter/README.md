# Experiments with jupyter-notebook

Trying to document experiments on embedding a jupyter notebooks into the geppetto webapp.

## Virgo + Tornado / subdomains
As a first approach, and to have a launchpad from where to prototype /
experiment, we have decided to have an iframe inside the main geppetto webapp
pointing to the web page hosted by the default jupyter notebook server.

Since we want to acccess js from the geppetto side from the jupyter side
(iframe), it is convenient to have both servers (virgo for geppetto, and
tornado for jupyter) on the same domain. That can be achived via virtual hosts,
and we used nginx to set up a server, proxying Virgo@localhost:8080 to
main.gpt.org:9999 and Jupyter@localhost:8888 to python.gpt.org:9999 See the
relevant [nginx config file](nginx.conf) for more info.

Once nginx, virgo and tornado are running, the geppetto app can be accessed at
[](http://main.gpt.org:9999/org.geppetto.frontend/). In order to circumvent
javascript's same origin policies, we also need to set
`document.domain='gpt.org'` **at both geppetto and jupyter** js. (See
http://www.dyn-web.com/tutorials/iframes/postmessage/ for possible
alternatives which don't require same domain). After that, jupyter can
access geppetto's global namespace via `window.parent`.

