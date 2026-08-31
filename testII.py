import csv
from datetime import datetime
import requests


# --- CLASS DEFINITION ---
# Class to model an active solar monitoring site with state tracking
class SolarGridNode:

    def __init__(self, node_id, location_name, capacity_kw):
        # Initialize instance attributes (variables linked to this specific object)
        self.node_id = node_id
        self.location_name = location_name
        self.capacity_kw = capacity_kw

    def evaluate_output(self, cloud_cover_percent):
        """Calculates estimated solar generation based on real-time cloud cover percentage."""
        # Loop-like branching logic: derive capacity factor from sky clarity
        if cloud_cover_percent < 20:
            efficiency_factor = 0.95  # Clear sky efficiency
            status = "OPTIMAL"
        elif cloud_cover_percent < 70:
            efficiency_factor = 0.60  # Partial cloud cover
            status = "MODERATE"
        else:
            efficiency_factor = 0.25  # Heavy cloud cover
            status = "LOW_GENERATION"

        # Calculate active output in kilowatts
        active_output_kw = self.capacity_kw * efficiency_factor

        # Return a dictionary containing the node's metric assessment
        return {
            "node_id": self.node_id,
            "location": self.location_name,
            "cloud_cover": cloud_cover_percent,
            "estimated_output_kw": round(active_output_kw, 2),
            "status": status,
        }


# --- API FETCH FUNCTION ---
def fetch_douala_solar_data():
    """Fetches real-time cloud cover metric for Douala, Cameroon via Open-Meteo API."""
    # Coordinates for Douala, Cameroon
    url = "https://api.open-meteo.com/v1/forecast?latitude=4.0511&longitude=9.7679&current=cloud_cover"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # Send HTTP GET request to retrieve environmental metrics
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            # Parse the API response into a Python dictionary
            data = response.json()
            # Extract cloud cover value from the current field object
            return data.get("current", {}).get("cloud_cover", 50)
        else:
            print(
                f"API warning (Status {response.status_code}). Fallback cloud cover value used."
            )
            return 50  # Fallback default value if API returns non-200
    except requests.exceptions.RequestException as err:
        print(f"Network issue encountered: {err}. Fallback metric applied.")
        return 50  # Fallback value on network connection loss


# --- FILE HANDLING FUNCTION ---
def append_to_csv(log_data, filename="grid_telemetry.csv"):
    """Appends evaluated telemetry metrics directly into a local CSV spreadsheet file."""
    # Check if the file already exists to decide whether to write headers
    file_exists = False
    try:
        with open(filename, mode="r") as file:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Open file in append mode ('a') so existing logs are preserved
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header row if creating file for the first time
        if not file_exists:
            writer.writerow(
                [
                    "Timestamp",
                    "Node ID",
                    "Location",
                    "Cloud Cover (%)",
                    "Est Output (kW)",
                    "Status",
                ]
            )

        # Write data record
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                log_data["node_id"],
                log_data["location"],
                log_data["cloud_cover"],
                log_data["estimated_output_kw"],
                log_data["status"],
            ]
        )
    print(f"--> Successfully wrote telemetry record to local file '{filename}'.")


# --- MAIN PIPELINE EXECUTION ---
def main():
    print("=== STARTING CAPSTONE SYSTEM MONITORING PIPELINE ===")

    # Step 1: Fetch live network data via API
    current_cloud_cover = fetch_douala_solar_data()
    print(
        f"API Live Reading: Douala Regional Cloud Cover = {current_cloud_cover}%"
    )

    # Step 2: Instantiate multiple Class objects (Grid Array Nodes)
    nodes = [
        SolarGridNode(node_id="DLA-01", location_name="Akwa", capacity_kw=100),
        SolarGridNode(
            node_id="DLA-02", location_name="Bonanjo", capacity_kw=250
        ),
        SolarGridNode(
            node_id="DLA-03", location_name="Bapanda", capacity_kw=500
        ),
    ]

    # Step 3: Loop through node objects, run analysis, and log output to file
    print("\n--- Processing Solar Array Network ---")
    for node in nodes:
        # Calculate metric via class method
        metrics = node.evaluate_output(current_cloud_cover)

        # Print metrics to output terminal
        print(
            f"[{metrics['node_id']} - {metrics['location']}] "
            f"Output: {metrics['estimated_output_kw']} kW | Status: {metrics['status']}"
        )

        # Save record to disk CSV file
        append_to_csv(metrics)

    print("\n=== PIPELINE EXECUTION COMPLETE ===")


# Python entry point execution guard
if __name__ == "__main__":
    main()