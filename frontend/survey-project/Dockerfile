FROM node:20 AS builder

WORKDIR /app
COPY . .

RUN npm ci --force
RUN npm run build:prod

FROM nginx:alpine

COPY --from=builder /app/dist/survey-project/browser /home/site/wwwroot
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]