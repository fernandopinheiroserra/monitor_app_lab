# Master Alert - Application Monitoring Lab

Master Alert is a lab environment built in Docker, designed to monitor application health through heartbeat pings. The application uses MongoDB to store and track heartbeat metrics, providing insights into application uptime and availability through a real-time dashboard.

## Features

- **Real-Time Heartbeat Monitoring**: Receives pings from monitored applications every 30 seconds, storing metadata and timestamps.
- **MongoDB Storage**: Stores heartbeat data and outage logs in MongoDB for reliable data tracking.
- **Dashboard Visualization**: Displays real-time data, including the uptime status of monitored apps, recent pings, and uptime metrics.
- **Automatic Collection Creation**: Initializes collections automatically in MongoDB if they don't already exist, ensuring seamless setup.
- **Docker-Based Lab Environment**: Easily deployable in a Docker environment, with the application and MongoDB containerized for portability and convenience.

## Technology Stack

- **Python & FastAPI**: The backend API to manage and receive heartbeat pings.
- **MongoDB**: NoSQL database to store uptime metrics and ping history.
- **Docker**: Containerized environment for easy deployment and scalability.
- **HTML/CSS**: Basic front-end for the dashboard, styled for readability.

## Requirements

Ensure you have the following installed:
- Docker
- Docker Compose (recommended for ease of setup)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/master-alert
   cd master-alert
   ```

2. **Configure MongoDB Connection**:
   Update the `initialize_db.py` and `main.py` to reflect your MongoDB container IP (e.g., `172.18.0.17`).

3. **Docker Compose Setup**:
   Use `docker-compose.yml` to create the application and MongoDB containers on the same network for seamless communication. 
   
   Sample `docker-compose.yml`:
   ```yaml
   version: '3'
   services:
     mongo:
       image: mongo:latest
       container_name: mongodb
       ports:
         - "27017:27017"
       networks:
         - app-network
     app:
       build: .
       container_name: master-alert
       depends_on:
         - mongo
       environment:
         - MONGO_HOST=mongodb
         - MONGO_PORT=27017
       networks:
         - app-network

   networks:
     app-network:
       driver: bridge
   ```

4. **Run the Docker Containers**:
   ```bash
   docker-compose up -d
   ```

   This will start both MongoDB and the Master Alert application in Docker containers.

5. **Access the Application**:
   - **API Endpoint**: Visit `http://localhost:9090/ping` to send heartbeat pings (replace with your IP if on a different setup).
   - **Dashboard**: Access the dashboard at `http://localhost:9090/` to view application metrics and uptime status.

## API Endpoints

- **/ping**: Receives a heartbeat ping from the monitored application with query parameters:
  - `empresa`: The name of the application sending the ping.
  - `sinc`: The name of the synchronizer or system component.

  Example request:
  ```bash
  curl "http://localhost:9090/ping?empresa=yourapp&sinc=component"
  ```

- **/status**: Retrieves the current system status, checking if any application missed its heartbeat.

- **/metrics/uptime_history**: Provides historical uptime data, useful for tracking application performance over time.

## Sample Dashboard View

- **Current Status**: Displays whether the heartbeat is active or missed.
- **Recent Pings**: Shows the last five pings received, including IP, application name, and sync component.
- **Uptime Metrics**: A graphical display (optional) of uptime percentage over a set time period.

## Troubleshooting

1. **Connection Issues**: Ensure MongoDB and Master Alert containers are on the same Docker network.
2. **Docker Logs**: Use `docker logs master-alert` or `docker logs mongodb` to view application logs and debug any connection issues.

## Future Enhancements

- **Detailed Analytics**: Enhance the dashboard to display historical uptime and outage statistics.
- **WebSocket Integration**: Real-time updates on the dashboard using WebSocket.
- **Scalability**: Add support for more applications to monitor in a clustered environment.

---

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, feel free to reach out to the repository owner.

