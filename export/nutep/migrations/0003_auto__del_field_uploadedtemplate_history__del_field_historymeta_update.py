# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UploadedTemplate.history'
        db.delete_column('nutep_uploadedtemplate', 'history_id')

        # Deleting field 'HistoryMeta.updated'
        db.delete_column('nutep_historymeta', 'updated')

        # Deleting field 'HistoryMeta.updated_by'
        db.delete_column('nutep_historymeta', 'updated_by_id')

        # Deleting field 'HistoryMeta.created'
        db.delete_column('nutep_historymeta', 'created')

        # Deleting field 'HistoryMeta.modificated'
        db.delete_column('nutep_historymeta', 'modificated')

        # Deleting field 'HistoryMeta.created_by'
        db.delete_column('nutep_historymeta', 'created_by_id')

        # Adding field 'HistoryMeta.content_type'
        db.add_column('nutep_historymeta', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'HistoryMeta.object_id'
        db.add_column('nutep_historymeta', 'object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'HistoryMeta.is_created'
        db.add_column('nutep_historymeta', 'is_created',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'HistoryMeta.data'
        db.add_column('nutep_historymeta', 'data',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HistoryMeta.user'
        db.add_column('nutep_historymeta', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, on_delete=models.PROTECT, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'UploadedTemplate.history'
        db.add_column('nutep_uploadedtemplate', 'history',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['nutep.HistoryMeta'], unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'HistoryMeta.updated'
        db.add_column('nutep_historymeta', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'HistoryMeta.updated_by'
        db.add_column('nutep_historymeta', 'updated_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='updators', null=True, to=orm['auth.User'], on_delete=models.PROTECT, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HistoryMeta.created'
        raise RuntimeError("Cannot reverse this migration. 'HistoryMeta.created' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HistoryMeta.created'
        db.add_column('nutep_historymeta', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HistoryMeta.modificated'
        raise RuntimeError("Cannot reverse this migration. 'HistoryMeta.modificated' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HistoryMeta.modificated'
        db.add_column('nutep_historymeta', 'modificated',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'HistoryMeta.created_by'
        raise RuntimeError("Cannot reverse this migration. 'HistoryMeta.created_by' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'HistoryMeta.created_by'
        db.add_column('nutep_historymeta', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='creators', on_delete=models.PROTECT, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'HistoryMeta.content_type'
        db.delete_column('nutep_historymeta', 'content_type_id')

        # Deleting field 'HistoryMeta.object_id'
        db.delete_column('nutep_historymeta', 'object_id')

        # Deleting field 'HistoryMeta.is_created'
        db.delete_column('nutep_historymeta', 'is_created')

        # Deleting field 'HistoryMeta.data'
        db.delete_column('nutep_historymeta', 'data')

        # Deleting field 'HistoryMeta.user'
        db.delete_column('nutep_historymeta', 'user_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'nutep.historymeta': {
            'Meta': {'object_name': 'HistoryMeta'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'data': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'nutep.uploadedtemplate': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'UploadedTemplate'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'http_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True', 'blank': 'True'}),
            'xml_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['nutep']