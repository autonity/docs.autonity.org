# Copyright (C) 2015-2024 Clearmatics Technologies Ltd - All Rights Reserved.

import logging
import os

DEBUG = os.environ.get("DEBUG") in ("1", "true", "True")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(name)s: %(message)s")
