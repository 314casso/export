# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BaseError.code'
        db.alter_column('nutep_baseerror', 'code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'BaseError.field'
        db.alter_column('nutep_baseerror', 'field', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'BaseError.date'
        db.alter_column('nutep_baseerror', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'BaseError.code'
        raise RuntimeError("Cannot reverse this migration. 'BaseError.code' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'BaseError.code'
        db.alter_column('nutep_baseerror', 'code', self.gf('django.db.models.fields.CharField')(max_length=50))

        # User chose to not deal with backwards NULL issues for 'BaseError.field'
        raise RuntimeError("Cannot reverse this migration. 'BaseError.field' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'BaseError.field'
        db.alter_column('nutep_baseerror', 'field', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'BaseError.date'
        db.alter_column('nutep_baseerror', 'date', self.gf('django.db.models.fields.DateTimeField')())

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
        'nutep.baseerror': {
            'Meta': {'object_name': 'BaseError'},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '3', 'db_index': 'True', 'blank': 'True'})
        },
        'nutep.container': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Container'},
            'SOC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cargo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'containers'", 'to': "orm['nutep.Draft']"}),
            'gross': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Line']", 'null': 'True', 'blank': 'True'}),
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
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contracts'", 'to': "orm['nutep.Line']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'startdate': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'terminal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Terminal']"})
        },
        'nutep.draft': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Draft'},
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
            'template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'drafts'", 'to': "orm['nutep.UploadedTemplate']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
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
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'nutep.readiness': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Readiness'},
            'done': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'readiness'", 'to': "orm['nutep.Draft']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'})
        },
        'nutep.terminal': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Terminal'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'nutep.uploadedtemplate': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'UploadedTemplate'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nutep.Contract']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'http_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True', 'blank': 'True'}),
            'voyage': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'templates'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': "orm['nutep.Voyage']"}),
            'xml_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'nutep.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nutep.Line']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'nutep.vessel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Vessel'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'})
        },
        'nutep.voyage': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Voyage'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'etd': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'db_index': 'True'}),
            'vessel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'voyages'", 'null': 'True', 'to': "orm['nutep.Vessel']"})
        }
    }

    complete_apps = ['nutep']