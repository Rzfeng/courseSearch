#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib')
import os

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


#render templates in directory
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/', 'search',
        '', 'search',
        '/search', 'search'
        )

class search:



    def GET(self):
        return render_template('search.html')

    def POST(self):
        post_params = web.input()

        courseList = {'statistics': 'STAT',
        'stat': 'STAT',
        'statistic': 'STAT',
        'cs': 'COMP SCI',
        'computer science': 'COMP SCI'}

        subject = str(post_params['subject']).lower()
        courseID = post_params['courseID']
        sectionID = post_params['sectionID']
        year = post_params['year']

        executeSearch = False
        if courseID != '':
            try:
                courseID = int(courseID)
                executeSearch = True
            except ValueError:
                return render_template('search.html')

        if sectionID != '':
            try:
                sectionID = int(sectionID)
                executeSearch = True
            except ValueError:
                return render_template('search.html')

        if sectionID != '':
            try:
                sectionID = int(sectionID)
                executeSearch = True
            except ValueError:
                return render_template('search.html')

        if subject != '':
            for search in subject.split():
                if search in courseList:
                    subject = courseList[search]
                    items = sqlitedb.getCourseInfo(subject, courseID, sectionID, year)
                    return render_template('search.html', search_result = items)

        if executeSearch == True:
            items = sqlitedb.getCourseInfo(subject, courseID, sectionID, year)
            return render_template('search.html', search_result = items)
            
        return render_template('search.html')


##########################Run Page##########################


if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
