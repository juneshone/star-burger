FROM node:15.8-alpine3.11
WORKDIR /opt/star-burger
COPY . .
RUN npm ci --dev
CMD ["./node_modules/.bin/parcel", "build", "bundles-src/index.js", "--dist-dir", "bundles", "--public-url=./"]


