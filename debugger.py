import os

import debugpy


def enable_debugger_if():
    if os.getenv("ENABLE_DEBUGGER") == "True":

        debugpy.listen(("0.0.0.0", 5678))
        print("Waiting for debugger attach...")
        debugpy.wait_for_client()
