FROM maven:3.9.9-eclipse-temurin-21 AS build
ARG MODULE
WORKDIR /work
COPY . .
RUN mvn -B -pl "${MODULE}" -am -DskipTests package && cp "${MODULE}/target/${MODULE}-1.0.0-SNAPSHOT.jar" /work/server.jar
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /work/server.jar /app/server.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/server.jar"]
