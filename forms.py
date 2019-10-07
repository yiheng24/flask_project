import wtforms
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import ValidationError

def keywords_vaild(form,feild):
    data=feild.data
    keywords=['admin','GM','管理员','fuck']
    if data in keywords:
        raise ValidationError('命名方式不符合规范')


class TaskFrom(FlaskForm):
    name=wtforms.StringField(
        render_kw={
            'class':'form-control',
            'placeholder':'任务名称'
        },
        validators=[
            validators.data_required('不可以为空'),
            keywords_vaild
        ]
    )
    description=wtforms.StringField(
        render_kw={
            'class': 'form-control',
            'placeholder': '任务描述'
        }
    )
    time=wtforms.DateField(
        render_kw={
            'class': 'form-control',
            'placeholder': '任务时间'
        }
    )
    public=wtforms.StringField(
        render_kw={
            'class': 'form-control',
            'placeholder': '任务发布人'
        }
    )