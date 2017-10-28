import os.path as osp

from uuid import UUID

from django.db.models import F
from django.utils.translation import ugettext as _
from misago.threads.api.postingendpoint import PostingMiddleware
from misago.threads.api.postingendpoint import PostingEndpoint
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Attachment
from misago.categories.models import Category
from rest_framework import serializers


from .conf import settings
from .models import Problem, Solution
from .utils import get_problem_uid, extract_problem_kwargs
from .tasks import run_judge


class OJSubmissionSerializer(serializers.Serializer):
    post = serializers.CharField()

    def validate_post(self, content):
        self.validate_attachments()
        starter = self.context['starter']
        thread = self.context['thread']
        uid = self.context['uid']
        ps = Problem.objects.filter(uid=UUID(uid))
        if ps.count() == 0:
            raise serializers.ValidationError(_('No such problem'))
        problem = ps[0]
        self.problem = problem
        sol = Solution.objects.filter(problem=problem, starter=starter)
        self.solution = None
        if sol.exists():
            solution = sol[0]
            if solution.thread != thread:
                raise serializers.ValidationError(_(
                    'Only one solution should be '
                    'submitted to the same problem'))
            self.solution = solution

    def validate_attachments(self):
        ids = self.context['attachments']
        attachments = Attachment.objects.filter(id__in=ids)
        if len(attachments) == 0:
            raise serializers.ValidationError(_('Must provide a attachment'))
        elif len(attachments) != 1:
            raise serializers.ValidationError(
                _('Only one attachment required'))
        upfile = attachments[0]
        if str(upfile.filetype) != 'ZIP':
            raise serializers.ValidationError(_('Only support ZIP file'))
        self.subject_path = osp.join(settings.MEDIA_ROOT, str(upfile.file))

    def post_save(self):
        problem = self.problem
        solution = self.solution
        starter = self.context['starter']
        thread = self.context['thread']
        if solution is None:
            solution = Solution.objects.create(problem=problem,
                                               starter=starter,
                                               thread=thread)
        solution.submit_counter = F('submit_counter') + 1
        solution.save()

        problem_attachments = problem.thread.first_post.attachments
        target_id = None
        for a in problem_attachments:
            if a['filetype'] == 'SIEZIP':
                target_id = a['id']
                break
        target_path = Attachment.objects.get(id=target_id).file
        target_path = osp.join(settings.MEDIA_ROOT, str(target_path))
        run_judge.delay(thread.id, solution.id, self.subject_path,
                        problem.module_name, target_path, problem.judge_name,
                        problem.order_type)


class OJSubmissionMiddleware(PostingMiddleware):
    def get_serializer(self):
        return OJSubmissionSerializer(
            data=self.request.data,
            context={
                'mode': self.mode,
                'post': self.post,
                'thread': self.thread,
                'starter': self.user,
                'attachments': self.request.data['attachments'],
                'uid': get_problem_uid(self.request.data['post']),
            }
        )

    def use_this_middleware(self):
        if self.mode == PostingEndpoint.EDIT:
            is_sub_cate = str(self.post.category) == settings.OJ_SUB_CATE_NAME
        elif self.mode == PostingEndpoint.START:
            cate_id = self.request.data['category']
            is_sub_cate = Category.objects.filter(
                id=cate_id, name=settings.OJ_SUB_CATE_NAME).count() == 1
        else:
            is_sub_cate = False
        uid = get_problem_uid(self.request.data['post'])
        if is_sub_cate and self.post.is_first_post and uid is not None:
            return True
        return False

    def post_save(self, serializer):
        serializer.post_save()


class OJReleaseSerializer(serializers.Serializer):
    post = serializers.CharField()

    def validate_attachments(self):
        ids = self.context['attachments']
        attachments = Attachment.objects.filter(id__in=ids)
        siezip_cnt = 0
        for upfile in attachments:
            if str(upfile.filetype) == 'SIEZIP':
                siezip_cnt += 1
        if siezip_cnt != 1:
            raise serializers.ValidationError(
                _('Requires one SIEZIP file'))

    def validate_post(self, content):
        self.validate_attachments()
        try:
            order_type, judge_name, module_name = extract_problem_kwargs(
                content)
        except Exception as e:
            raise serializers.ValidationError(_('Judge argument error'))
        self.order_type = order_type
        self.judge_name = judge_name
        self.module_name = module_name

    def save(self):
        thread = self.context['thread']
        starter = self.context['user']
        post = self.context['post']
        problem, created = Problem.objects.get_or_create(
            thread=thread, starter=starter)
        uid = problem.uid
        uid_str = settings.OJ_UID_FORMAT.format(uid.hex)
        problem.order_type = self.order_type
        problem.judge_name = self.judge_name
        problem.module_name = self.module_name + '.py'
        problem.save()
        post.parsed = post.parsed + '\n' + uid_str
        update_post_checksum(post)
        post.save()


class OJReleaseMiddleware(PostingMiddleware):
    def get_serializer(self):
        return OJReleaseSerializer(
            data=self.request.data,
            context={
                'mode': self.mode,
                'post': self.post,
                'thread': self.thread,
                'user': self.user,
                'attachments': self.request.data['attachments'],
            }
        )

    def use_this_middleware(self):
        ids = self.request.data['attachments']
        attachments = Attachment.objects.filter(id__in=ids)
        sie_zips = [f for f in attachments if str(f.filetype) == 'SIEZIP']
        if not sie_zips:
            return False
        if self.mode == PostingEndpoint.EDIT:
            is_rel_cate = str(self.post.category) == settings.OJ_CATE_NAME
        elif self.mode == PostingEndpoint.START:
            cate_id = self.request.data['category']
            is_rel_cate = Category.objects.filter(
                id=cate_id, name=settings.OJ_CATE_NAME).count() == 1
        else:
            is_rel_cate = False
        if is_rel_cate and self.post.is_first_post:
            return True
        return False

    def save(self, serializer):
        serializer.save()
