#!/bin/bash
mongorestore -h localhost --nsInclude 'rarbg.*' --dir /rarbg
exit 0