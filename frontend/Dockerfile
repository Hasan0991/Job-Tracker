FROM node:20 as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20

RUN npm install -g serve

WORKDIR /app

COPY --from=build /app/build /app/build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
