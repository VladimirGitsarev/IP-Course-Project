FROM node:alpine
WORKDIR /front

COPY package.json .

RUN npm install

COPY . .
CMD npm start
