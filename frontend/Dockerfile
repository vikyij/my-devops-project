FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

# Expose the port for development
EXPOSE 3000

CMD ["npm", "start"] 