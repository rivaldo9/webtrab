# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

from google.appengine.ext import ndb

def int_validator(prop, val):
	if(val):
		val = int(val)
		return val

class Disciplina(ndb.Model):
	nome = ndb.StringProperty(required=True)
	periodo = ndb.StringProperty(required=True)

class Professor(ndb.Model):
	nome = ndb.StringProperty(required=True)
	area = ndb.StringProperty(required=True)
	perfil = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	foto = ndb.BlobProperty(required=False)

class Cursos(ndb.Model):
	nome = ndb.StringProperty(required=True)
	periodo = ndb.StringProperty(required=True)
	semestral = ndb.StringProperty(required=True)
	disciplinas = ndb.StructuredProperty(Disciplina, repeated=True)