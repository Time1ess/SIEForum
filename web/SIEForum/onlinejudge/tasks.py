import time
import tempfile
import zipfile
import os
import shutil
import functools
import importlib.util as import_util

from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from misago.threads.models import Thread, Post
from misago.threads.checksums import update_post_checksum

from . import SOL_ERROR, SOL_FINISHED, SOL_RUNNING, LOW_SCORE_FIRST
from . import judges
from .conf import settings
from .models import Solution


logging = get_task_logger(__name__)


def judge_wraps(func):
    @functools.wraps(func)
    def _wraps(self, thread_id, sol_id, *args, **kwargs):
        start_time = time.time()
        try:
            logging.info('Judging started:{}'.format(sol_id))
            solution = Solution.objects.get(id=sol_id)
            result = func(solution, *args, **kwargs)
        except Exception as e:
            logging.error('Judgin failed:{}'.format(e))
            solution.status = SOL_ERROR
            result = -1
        else:
            logging.info('Judging succeed:{}'.format(sol_id))
            solution.status = SOL_FINISHED
        finally:
            solution.save()
            logging.info('Judging finished:{}'.format(sol_id))
        # Reply thread about judgement details
        duration = time.time() - start_time
        try:
            thread = Thread.objects.get(id=thread_id)
            poster = get_user_model().objects.get(username='ROBOT')
            now = timezone.now()
            reply = settings.OJ_REPLY_FORMAT % {
                'status': _('Error') if result < 0 else _('Succeed'),
                'duration': duration,
                'result': result,
                'updated_on': timezone.localtime(now).strftime(
                    _('%Y-%m-%d %H:%M:%S')),
            }
            post = Post.objects.filter(
                category=thread.category,
                thread=thread,
                poster=poster)
            if post.count() == 0:
                post = Post(
                    category=thread.category,
                    thread=thread,
                    poster=poster,
                    poster_name=settings.OJ_ROBOT_NAME,
                    poster_ip='0.0.0.0',
                    updated_on=now,
                    original=reply,
                    parsed=reply,
                    posted_on=now)
            else:
                post = post[0]
                post.updated_on = now
                post.original = reply
                post.parsed = reply
            post.save()
            update_post_checksum(post)
            post.save()
        except Exception as e:
            logging.error('Posting error:{}'.format(e))
        return result
    return _wraps


@shared_task(bind=True, time_limit=settings.OJ_TIME_LIMITS)
@judge_wraps
def run_judge(solution, subject_zip_path, module_name,
              target_zip_path, evaluate_fname, order_type,
              module_func='predict'):
    evaluate = getattr(judges, evaluate_fname)
    solution.status = SOL_RUNNING
    solution.save()
    subject_fname = subject_zip_path.rsplit('/', 1)[-1]
    target_fname = target_zip_path.rsplit('/', 1)[-1]

    # Work in temporary directory
    tmp_dir = tempfile.gettempdir()
    os.chdir(tmp_dir)

    shutil.copy(subject_zip_path, '.')
    zf = zipfile.ZipFile(subject_fname)
    zf.extractall()

    shutil.copy(target_zip_path, '.')
    zf = zipfile.ZipFile(target_fname)
    zf.extractall()

    # Load target module
    spec = import_util.spec_from_file_location("target", 'evaluate.py')
    target = import_util.module_from_spec(spec)
    spec.loader.exec_module(target)

    # Load subject module
    spec = import_util.spec_from_file_location("subject", module_name)
    subject = import_util.module_from_spec(spec)
    spec.loader.exec_module(subject)

    # Get output from target.INPUTS and compare with target.OUTPUTS
    output = getattr(subject, module_func)(*target.INPUTS)
    result = evaluate(output, *target.OUTPUTS)
    # Update with better results
    if order_type == LOW_SCORE_FIRST:
        if solution.result >= 0:
            solution.result = min(solution.result, result)
        else:
            solution.result = result
    else:
        solution.result = max(solution.result, result)
    return result
