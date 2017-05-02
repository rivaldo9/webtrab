# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, invalid-name, import-error

import os
import jinja2
import webapp2

from google.appengine.api import images
from google.appengine.ext import ndb

from model import Professor
from model import Cursos
from model import Disciplina

from time import sleep

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        professor_key = ndb.Key(urlsafe=self.request.get('img_id'))
        professor = professor_key.get()
        if professor.foto:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(professor.foto)
        else:
            self.response.out.write('Imagem não encontrada')

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('id'))
        key.delete()
        sleep(.1)
        if(self.request.get('page') == 'professor'):
            self.redirect('professor')
        else:
            self.redirect('/cursos')

class UpdateHandler(Handler):
    def get(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        if(self.request.get('page') == 'professor'):
            professor = key.get()
            self.render("update_professor.html", professor=professor)
        else:
            curso = key.get()
            self.render("update_curso.html", curso=curso)
    
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('key'))
        if(self.request.get("page") == 'professor'):
            professor = key.get()
            professor.nome   = self.request.get('nome')
            professor.area   = self.request.get('area')
            professor.perfil = self.request.get('perfil')
            professor.email  = self.request.get('email')
            professor.put()
            sleep(.1)
            self.redirect("/professor")
        else:
            curso = key.get()
            curso.nome = self.request.get('nome')
            curso.periodo = self.request.get('periodo')
            curso.semestral = self.request.get('semestral')
            curso.put()
            sleep(.1)
            self.redirect('/cursos')


class MainHandler(Handler):
    def get(self):
        self.render("index.html")

class ProfessorHandler(Handler):
    def get(self):
        professores = Professor.query().order(Professor.nome)
        self.render("professor.html", professores=professores)

    def post(self):
        nome   = self.request.get("nome")
        area   = self.request.get("area")
        perfil = self.request.get("perfil")
        email  = self.request.get("email")
        foto   = self.request.get("img")
        professor = Professor(nome=nome, area=area, perfil=perfil,
                              email=email, foto=foto)
        professor.put()
        sleep(.1)
        return self.redirect('/professor')

class CursoHandler(Handler):
	def get(self):
		cursos = Cursos.query().order(Cursos.nome)
		self.render("cursos.html", cursos=cursos)

	def post(self):
		nome 	   = self.request.get("nome")
		periodo    = self.request.get("periodo")
		semestral  = self.request.get("semestral")
		disciplina = self.request.get("disciplinas")

		curso = Cursos(nome=nome, periodo=periodo, semestral=semestral, disciplinas=[Disciplina(nome='Bla', periodo='1'), Disciplina(nome='Bla', periodo='1'), Disciplina(nome='Bla', periodo='1')])
		curso.put()
		sleep(.1)
		return self.redirect('/cursos')

class DisciplinasHandler(Handler):
    def get(self):
        curso_key = ndb.Key(urlsafe=self.request.get('key'))
        disciplinas = curso_key.get().disciplinas
        self.render('disciplinas.html', disciplinas=disciplinas)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/professor', ProfessorHandler),
    ('/img', ImageHandler),
    ('/cursos', CursoHandler),
    ('/delete', DeleteHandler),
    ('/update', UpdateHandler),
    ('/disciplinas', DisciplinasHandler)
], debug=True)
