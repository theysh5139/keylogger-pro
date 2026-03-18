from gui import launch
import os

if __name__ == "__main__":
    # Ensure logs folder exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    print("Starting User Activity Monitor...")
    launch()