# Dummy root Dockerfile
FROM alpine:3.18

# This is just a placeholder so that Sliplane/Nixpacks doesn't fail
# Your real builds are defined in docker-compose.yml
CMD ["echo", "This is a dummy Dockerfile. Use docker-compose to run services."]
