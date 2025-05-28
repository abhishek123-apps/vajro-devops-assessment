import docker
import time
import logging
import signal
import sys

# Configuration
CPU_THRESHOLD = 80.0  # in percent
POLL_INTERVAL = 5     # in seconds

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("docker_monitor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Graceful Exit
def handle_exit(signum, frame):
    logging.info("Received exit signal. Exiting gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def get_cpu_percent(stats):
    """
    Calculate CPU usage percentage using Docker stats.
    """
    try:
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                       stats["precpu_stats"]["system_cpu_usage"]
        if system_delta > 0 and cpu_delta > 0:
            cpu_count = len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", []))
            return (cpu_delta / system_delta) * cpu_count * 100.0
        return 0.0
    except KeyError:
        logging.warning("Could not calculate CPU usage.")
        return 0.0

def monitor_containers():
    """
    Monitor all running containers and check their CPU usage.
    """
    try:
        client = docker.from_env()
        while True:
            containers = client.containers.list()   #This line list the running containers using SDK 
            if not containers:
                logging.info("No running containers.")
            for container in containers:
                try:
                    stats = container.stats(stream=False)
                    cpu_usage = get_cpu_percent(stats)
                    logging.info(f"Container {container.name} CPU Usage: {cpu_usage:.2f}%")
                    if cpu_usage > CPU_THRESHOLD:
                        logging.warning(f"High CPU Usage: {container.name} - {cpu_usage:.2f}%")
                        simulate_alert(container.name, cpu_usage)
                except Exception as e:
                    logging.error(f"Error fetching stats for container {container.name}: {e}")
            time.sleep(POLL_INTERVAL)
    except docker.errors.DockerException as e:
        logging.error(f"Docker connection failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def simulate_alert(container_name, cpu_usage):
    """
    Simulate alerting logic - currently just logs.
    """
    logging.error(f"ALERT: Container '{container_name}' exceeded CPU threshold with {cpu_usage:.2f}%")

if __name__ == "__main__":
    logging.info("Starting Docker CPU usage monitor...")
    monitor_containers()

