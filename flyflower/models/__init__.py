from tortoise import models, fields


class Poetry(models.Model):
    """诗词"""

    id = fields.IntField(pk=True)
    author = fields.CharField(max_length=32, null=True)
    rhythmic = fields.CharField(max_length=128, null=True)
    paragraphs = fields.JSONField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """元数据"""

        table = "poetry"
