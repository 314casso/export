# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Draft.voyage'
        db.add_column('nutep_draft', 'voyage',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='drafts', null=True, to=orm['nutep.Voyage']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Draft.voyage'
        db.delete_column('nutep_draft', 'voyage_id')


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
        'nutep.container': {
            'Meta': {'object_name': 'Container'},
            'SOC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'containers'", 'to': "orm['nutep.Draft']"}),
            'gross': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Voyage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_index': 'True'}),
            'netto': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'tare': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'})
        },
        'nutep.contract': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Contract'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expired': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contracts'", 'to': "orm['nutep.Line']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'startdate': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'terminal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Terminal']"})
        },
        'nutep.draft': {
            'Meta': {'object_name': 'Draft'},
            'POD': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'POL': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'consignee': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'finalDestination': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'finstatus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Line']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'notify': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'poruchenie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'poruchenieNums': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'shipper': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.UploadedTemplate']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'vessel': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'drafts'", 'null': 'True', 'to': "orm['nutep.Voyage']"})
        },
        'nutep.historymeta': {
            'Meta': {'object_name': 'HistoryMeta'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'})
        },
        'nutep.line': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Line'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'nutep.terminal': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Terminal'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'nutep.uploadedtemplate': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'UploadedTemplate'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'http_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Voyage']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'xml_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'nutep.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nutep.Line']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'nutep.voyage': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Voyage'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'})
        }
    }

    complete_apps = ['nutep']