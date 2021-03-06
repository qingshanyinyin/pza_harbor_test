#!/usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
from time import time
from time import sleep
from threading import Thread
from Queue import Queue
import os
import argparse

begin = 1
iterations = 10
concurrency = 30
# repo_address = "your-docker-registry-domain"
# lxy edit
repo_address = "10.7.11.211:5000/"
images1 = [repo_address + "tensorflow/tensorflow:v",repo_address + "pytorch/pytorch:v",repo_address + "caffe/caffe:v",repo_address + "mxnet/mxnet:v"]

# lxy edit
repo_ref = "tensorflow"
repo_url = repo_address + repo_ref

# lxy edit
image_name = "tensorflow"

# 存放Dockerfile的工作目录
work_dir = "containers/nginx"

# 记录文件
build_results_file = "build_results.csv" # build镜像
push_results_file = "push_results.csv"   # push镜像
pull_results_file = "pull_results.csv"   # pull镜像
delete_local_results_file = "delete_local_results.csv"  # 删除镜像

# 记录文件，pull
results_files = [pull_results_file]

for results_file in results_files:
    outfile = open(results_file, 'w')
    outfile.write("iteration,succeed or not,spent_time")
    outfile.close()

work_queue = Queue()

# push 全路径
imagePrefix = repo_url + '/' + image_name + ':v'

# 构建镜像
def build_container(iteration):
    # 记录构建初始时间
    start_time = time()
    # 构建镜像
    build_command = Popen(['docker', 'build', '--no-cache=true', '-t', imagePrefix + str(iteration), '--file=' + work_dir + '/dockerfile', work_dir])
    # 等待
    ret_code = build_command.wait()
    # 结束时间
    end_time = time()
    # 构建时间
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(build_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()

# 推镜像
def push_container(iteration):
    start_time = time()
    push_command = Popen(['docker', 'push', imagePrefix + str(iteration)])
    ret_code = push_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(push_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()

def push_container_lxy(iteration,imagePrefix):
    start_time = time()
    push_command = Popen(['docker', 'push', imagePrefix + str(iteration)])
    ret_code = push_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(push_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()


def delete_local_images(iteration):
    start_time = time()
    delete_local_images_command = Popen(['docker', 'rmi', imagePrefix + str(iteration)])
    ret_code = delete_local_images_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(delete_local_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()


def pull_container(iteration):
    start_time = time()
    pull_command = Popen(['docker', 'pull', imagePrefix + str(iteration)])
    ret_code = pull_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(pull_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()

def tag_container(iteration):
    images = "tensorflow/tensorflow:20.09-py3-cuda11"
    start_time = time()
    pull_command = Popen(['docker', 'tag',images,imagePrefix + str(iteration)])
    ret_code = pull_command.wait()
    end_time = time()
    action_time = end_time - start_time
    flag = "true"
    if ret_code == 0:
        print
        "Iteration", iteration, "has been done in", action_time, "successfully"
    else:
        print
        "Iteration", iteration, "has been done in", action_time, "failure"
        flag = "false"
    outfile = open(pull_results_file, 'a')
    outfile.write('\n' + str(iteration) + "," + flag + "," + str(int(action_time)))
    outfile.close()


def repeat():
    if work_queue.empty() is False:
        iteration = work_queue.get_nowait()
        container_action(iteration)
        work_queue.task_done()

def repeat_lxy():
    if work_queue.empty() is False:
        iteration = work_queue.get_nowait()
        container_action(iteration,imagePrefix1)
        work_queue.task_done()


def fill_queue(iterations):
    for iteration in range(begin, (iterations + 1)):
        work_queue.put(iteration)

#container_actions = [build_container, push_container, delete_local_images, pull_container,tag_container]
#container_actions = [delete_local_images]
container_actions = [push_container_lxy]


for container_action in container_actions:
    fill_queue(iterations)
    for thread_num in range(1, (concurrency + 1)):
        for imagePrefix1 in images1:
            if work_queue.empty() is True:
                break
            worker = Thread(target=repeat_lxy)
            worker.start()
    work_queue.join()
