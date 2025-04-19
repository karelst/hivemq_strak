


# RefreshWatchdog runs in a separate thread, constantly checking if the last refresh exceeds the timeout.
# If a refresh doesn't happen within the timeout, the action() function is called.
# Call refresh() at regular intervals to keep the watchdog from triggering.
# The stop() method allows stopping the watchdog manually.

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
        self.running = True
        self.thread = threading.Thread(target=self._watchdog, daemon=True)
        self.thread.start()

    def refresh(self):
        """Reset the watchdog timer by updating the last refresh time."""
        self.last_refresh = time.time()
       
    def _watchdog(self):
        """Check periodically if the refresh has stopped."""
        while self.running:
            time.sleep(self.timeout / 2)
            if time.time() - self.last_refresh > self.timeout:
                self.action()
                self.running = False  # Stop watchdog after action

    def stop(self):
        """Manually stop the watchdog."""
        self.running = False
        print("watchdog stop ")

    def default_action(self):
        """Default action when refresh stops."""
        print("Warning: Refresh stopped!")

# Example Usage
def on_refresh_stop():
    print(f"ALERT! Periodic refresh has stopped.  {datetime.now().time()}")
    watchdog.stop()
    
watchdog = RefreshWatchdog(timeout=5, action=on_refresh_stop)

# Simulating periodic refresh
try:
    i=0
    for _ in range(10):  # Simulating 10 refreshes
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
    print("Manual stop!")
    watchdog.stop()
