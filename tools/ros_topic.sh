#!/bin/bash

# 获取并加载ROS 2环境
load_ros_environment() {
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
}

# 显示ROS 2命令选项并获取用户选择
select_ros_command() {
    echo "请选择一个ROS 2话题命令 (输入序号):"
    options=(
        "bw:    显示话题的带宽"
        "delay: 显示话题的延迟"
        "echo:  输出话题消息"
        "hz:    显示发布话题的频率"
        "info:  显示话题信息"
    )
    for i in "${!options[@]}"; do
        echo "$((i + 1)). ${options[$i]}"
    done

    read -p "输入序号: " command_index
    case $command_index in
    1) command="bw" ;;
    2) command="delay" ;;
    3) command="echo" ;;
    4) command="hz" ;;
    5) command="info" ;;
    *)
        echo "无效的选择，请重新运行脚本。"
        exit 1
        ;;
    esac
}

# 显示ROS 2话题选项并获取用户选择
select_ros_topic() {
    all_topics=$(ros2 topic list)
    IFS=$'\n' read -r -d '' -a topics_array <<<"$all_topics"

    echo "请选择一个话题 (输入序号):"
    for i in "${!topics_array[@]}"; do
        echo "$((i + 1)). ${topics_array[$i]}"
    done

    read -p "输入序号: " topic_index
    if ! [[ "$topic_index" =~ ^[0-9]+$ ]] || [ "$topic_index" -lt 1 ] || [ "$topic_index" -gt "${#topics_array[@]}" ]; then
        echo "无效的选择，请重新运行脚本。"
        exit 1
    fi

    topic=${topics_array[$((topic_index - 1))]}
}

# 执行ROS 2命令
execute_ros_command() {
    echo "执行命令: ros2 topic $command $topic"
    ros2 topic $command $topic
}

# 主函数
main() {
    load_ros_environment

    if [ $# -eq 2 ]; then
        command=$1
        topic=$2
    elif [ $# -eq 1 ]; then
        command=$1
        select_ros_topic
    else
        select_ros_command
        select_ros_topic
    fi

    execute_ros_command
}

# 调用主函数
main "$@"
