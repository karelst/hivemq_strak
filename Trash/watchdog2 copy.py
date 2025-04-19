# start() method:

# Starts the watchdog if it's not already running.
# Resets last_refresh to ensure no immediate timeout.
# Creates and starts a new monitoring thread.
# stop() method:

# Now ensures the watchdog stops cleanly.
# Behavior:
# You can start the watchdog using watchdog.start().
# You can stop it anytime using watchdog.stop().
# If stopped and restarted, it behaves as if it was newly initialized.


import threading
import time
from datetime import datetime

class RefreshWatchdog:
    def __init__(self, timeout=5, action=None):
        """
        :param timeout: Time (seconds) after which, if no refresh signal is received, an action is taken.
        :param action: Function to call when refresh stops.
        """
        self.timeout = timeout
        self.action = action if action else self.default_action
        self.last_refresh = time.time()
        self.running = False
        self.thread = None

    def refresh(self):
        """Reset the watchdog timer by updating the last refresh time."""
        if self.running:
            print(f"---watchdog refresh {(time.time()-self.last_refresh):.2f} ")
            self.last_refresh = time.time()

    def _watchdog(self):
        """Check periodically if the refresh has stopped."""
        while self.running:
            time.sleep(self.timeout / 2)
            if time.time() - self.last_refresh > self.timeout:
                self.action()
                self.running = False  # Stop watchdog after action

    def start(self):
        """Start or restart the watchdog."""
        if not self.running:
            self.running = True
            self.last_refresh = time.time()
            self.thread = threading.Thread(target=self._watchdog, daemon=True)
            self.thread.start()
            print("---watchdog start ")

    def stop(self):
        """Manually stop the watchdog."""
        self.running = False
        print("---watchdog stop ")

    def default_action(self):
        """Default action when refresh stops."""
        print("---Warning: Refresh stopped!")

#
#####################################################################################

# Example Usage
def on_refresh_stop():
   print(f"ALERT! Periodic refresh has stopped.  {datetime.now().time()}")

if __name__ == "__main__":
    watchdog = RefreshWatchdog(timeout=5, action=on_refresh_stop)

    # Start the watchdog
    watchdog.start()

    # Simulating periodic refresh
    try:
        i=0
        for _ in range(6):  # Simulating 10 refreshes
            time.sleep(2)  # Refreshing every 2 seconds
            watchdog.refresh()
            # i=i+1
            i+=1
            #print(f"refresh {i}  {datetime.now().time()}")

        print("Stopping watchdog for 10 seconds...")
        watchdog.stop()
        time.sleep(10)  # Simulating pause

        print("Restarting watchdog...")
        watchdog.start()

        i=0
        for _ in range(6):  # Simulating 10 refreshes
            time.sleep(2)  # Refreshing every 2 seconds
            watchdog.refresh()
            # i=i+1
            i+=1
            print(f"refresh {i}  {datetime.now().time()}")

        print(f"refreshEND wait10 {datetime.now().time()}")
        time.sleep(10)  # Simulating a failure to refresh for 7 seconds
        print(f"10sec norefresh {datetime.now().time()}")
        watchdog.stop()

    except KeyboardInterrupt:
        watchdog.stop()
