import os
import datetime

branch_name = f"text_change/{datetime.datetime.now().timestamp()}"

os.system(f"git checkout -b {branch_name}")
