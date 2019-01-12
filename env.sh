#!/usr/bin/env bash

# Loads local.env into environment
export $(cat local.env | xargs)
