# Online Judge settings

from django.utils.translation import ugettext_lazy as _


OJ_CATE_NAME = 'OJ发布区'
OJ_SUB_CATE_NAME = 'OJ提交区'
OJ_NOTE_SIGN_FIRST = '↓'
OJ_NOTE_SIGN_SECOND = '↑'
OJ_NOTE_SIGN_NUM = 37
OJ_UID_FORMAT = (
    '<p>' +
    OJ_NOTE_SIGN_FIRST * OJ_NOTE_SIGN_NUM +
    '请复制以下加粗内容' +
    OJ_NOTE_SIGN_FIRST * OJ_NOTE_SIGN_NUM +
    '</p>' +
    '<h2>识别码:|{}|</h2>' +
    '<p>' +
    OJ_NOTE_SIGN_SECOND * OJ_NOTE_SIGN_NUM +
    '请复制以下加粗内容' +
    OJ_NOTE_SIGN_SECOND * OJ_NOTE_SIGN_NUM +
    '</p>')
OJ_UID_PATTERN = r'识别码:\|(.*?)\|'
OJ_RANKING_SIZE = 100
OJ_ROBOT_NAME = 'SIE-ROBOT'
OJ_REPLY_FORMAT = _(
    '<h3>Status: %(status)s!</h3>'
    '<h3>Finished in %(duration).4f s.</h3>'
    '<h3>Result: %(result).4f</h3>'
    '<h3>Updated: %(updated_on)s</h3>')
OJ_ORDER_KEY = '排序方式'
OJ_JUDGE_KEY = '评分类型'
OJ_MODULE_KEY = '执行模块'
OJ_DEFAULT_JUDGE = '默认值'
