#!/bin/bash

current_dir=$(cd $(dirname $0) && pwd)
install_dir=${current_dir}/../../
source_file=$(find $install_dir/share -type f -name "local_setup.bash")

if [ -z "$source_file" ]; then
  source_file=$(find /agibot -type f -name "local_setup.bash")
fi

if [ -z "$source_file" ]; then
  echo "未找到 $install_dir 和 /agibot 下的 local_setup.bash 文件，请检查目录是否正确"
  exit 1
fi

for file in $source_file; do
  source $file
done

# Function to handle ctrl+c
function finish {
  if [ -n "$PID" ]; then
    echo "Recording interrupted by user"
    kill $PID
    wait $PID 2>/dev/null
    echo "Recording completed: $BAG_PATH"
    echo "Recorded topics:"
    for TOPIC in "${TOPICS[@]}"; do
      echo "  - $TOPIC"
    done
    # Get additional information about the recorded bag file
    ros2 bag info $BAG_PATH

    # Package the bag file
    PACKAGE_NAME="${BAG_NAME}.tar.gz"
    tar -czf "${OUTPUT_DIR}/${PACKAGE_NAME}" -C "${OUTPUT_DIR}" "${BAG_NAME}"
    echo "Package created: ${OUTPUT_DIR}/${PACKAGE_NAME}"

    # Upload the package
    UPLOAD_URL="https://file.agibot.com/rosbag"
    curl -F "file=@${OUTPUT_DIR}/${PACKAGE_NAME}" $UPLOAD_URL
    echo "Upload completed: ${UPLOAD_URL}"

    PID=""
  fi
}

# Default values
DEFAULT_OUTPUT_DIR="./rosbag"
DEFAULT_TOPICS=(
  "/body_drive/neck_joint_state"
  "/body_drive/neck_joint_command"
  "/body_drive/waist_joint_state"
  "/body_drive/waist_joint_command"
  "/body_drive/lift_joint_state"
  "/body_drive/lift_joint_command"
  "/body_drive/arm_joint_state"
  "/body_drive/arm_joint_command"
  "/body_drive/wheel_joint_state"
  # "/body_drive/wheel_joint_command"
  "/ros2_debug/joint_states_active"
  "/ros2_debug/joint_commands_active"
  "/ros2_debug/joint_states_serial"
  "/ros2_debug/joint_commands_serial"
  # "/skill/arm_joint_state"
  "/ros2_debug/remote_data"
  "/ros2_debug/action"
)

# Parse arguments
OUTPUT_DIR="${1:-$DEFAULT_OUTPUT_DIR}"
shift
TOPICS=("$@")
if [ ${#TOPICS[@]} -eq 0 ]; then
  TOPICS=("${DEFAULT_TOPICS[@]}")
fi

# Generate bag file name based on current time
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BAG_NAME="rosbag_${TIMESTAMP}"
BAG_PATH="${OUTPUT_DIR}/${BAG_NAME}"

# Create the output directory if it does not exist
mkdir -p "$OUTPUT_DIR"

# Construct the ros2 bag record command
COMMAND="ros2 bag record -o ${BAG_PATH}"
for TOPIC in "${TOPICS[@]}"; do
  COMMAND="${COMMAND} ${TOPIC}"
done

# Start the recording process
eval $COMMAND &
PID=$!

# Trap ctrl+c and call finish function
trap finish SIGINT

# Wait indefinitely until interrupted
wait $PID

# Finish recording
finish
