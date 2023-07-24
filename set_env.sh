#!/bin/bash

export AIRFLOW_HOME="$(pwd)"

# issue : Task exited with return code Negsignal.SIGTRAP
# https://stackoverflow.com/questions/66012040/task-exited-with-return-code-negsignal-sigabrt-airflow-task-fails-with-snowflak
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
