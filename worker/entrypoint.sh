#!/bin/bash
cd /SIEForum
celery -A SIEForum.celery worker --concurrency=20 --loglevel=info
