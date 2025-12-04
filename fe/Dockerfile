FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache curl bash

RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"

COPY package.json ./
COPY bun.lock ./

RUN bun install

COPY . .

EXPOSE 3000

CMD ["bun", "run", "dev"]