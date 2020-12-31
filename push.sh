#!/bin/bash
python tf/test-repo-formal.py & python py/test-repo-formal.py & python mx/test-repo-formal.py & python cf/test-repo-formal.py & python pp/test-repo-formal.py
wait()
