@echo off
echo Stopping old containers...
docker-compose down

echo Building and starting containers...
docker-compose up -d --build

echo Waiting for MongoDB to be healthy...
:wait
FOR /F "tokens=*" %%i IN ('docker inspect --format="{{.State.Health.Status}}" my-app-mongo-1') DO set STATUS=%%i
IF "%STATUS%"=="healthy" (
    echo MongoDB is ready!
) ELSE (
    echo Waiting...
    TIMEOUT /T 2 >nul
    GOTO wait
)

echo Deployment finished! Your app should be running at http://localhost:8000
