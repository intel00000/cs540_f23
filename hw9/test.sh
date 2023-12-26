#!/bin/bash

# Variables
wins=0
total_runs=5
threshold_time=30
count_long_running=0

# Loop to run the Python script
for ((i=1; i<=$total_runs; i++)); do
    start_time=$(date +%s)
    output=$(python3 game.py)
    end_time=$(date +%s)
    execution_time=$((end_time - start_time))

    # Check if output contains "AI wins!"
    if [[ $output =~ "AI wins!" ]]; then
        echo "Run $i: AI wins!"
        ((wins++))
    else
        echo "Run $i: AI did not win."
    fi

    # Check if execution time is longer than the threshold
    if [ $execution_time -gt $threshold_time ]; then
        ((count_long_running++))
    fi

    echo "Execution time: $execution_time seconds"
    echo "-----------------------"
done

# Display summary
echo "Summary:"
echo "Number of runs where AI wins: $wins / $total_runs"
echo "Number of runs taking longer than $threshold_time seconds: $count_long_running"
```