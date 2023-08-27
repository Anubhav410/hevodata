from django.db.models import Model, CharField, DateTimeField, TextField, ForeignKey, DO_NOTHING


class GoogleCredentials(Model):
    token = CharField(max_length=500)
    refresh_token = CharField(max_length=500)
    token_uri = CharField(max_length=500)
    client_id = CharField(max_length=500, unique=True)
    client_secret = CharField(max_length=500)
    scopes = CharField(max_length=500)
    expiry = DateTimeField(null=True)
    created_at = DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Files(Model):
    client_id = CharField(max_length=500)
    file_name = CharField(max_length=400, null=True)
    source = CharField(max_length=40, null=True)
    source_file_id = CharField(max_length=400, null=True)
    mime_type = CharField(max_length=400, null=True)
    file_content = TextField(null=True)
    created_at = DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
