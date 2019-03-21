# setup (virtual environment):

    cd <folder containing "change_statistics">
    python3 -m venv stat-venv
    source stat-venv/bin/activate
    pip install pandas matplotlib numpy mpldatacursor

# usage examples:

    export PYTHONPATH=$PYTHONPATH:<folder containing "change_statistics">
    python3 change_statistics/intervalStatistics.py /home/example/changeLog_Tue_Nov_13_12:55:20_CET_2018.txt
