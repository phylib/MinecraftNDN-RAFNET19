# setup (virtual environment):

    python3 -m venv stat-venv
    source stat-venv/bin/activate
    pip install pandas matplotlib numpy mpldatacursor

# running the statistics script:

    source stat-venv/bin/activate
    export PYTHONPATH=$(dirname $(pwd))
    python3 intervalStatistics.py ../../data/gameStateChanges.txt
    deactivate
