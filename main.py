#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, cgi, jinja2, os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Blogpost(db.Model):
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    text = db.TextProperty(required = True)

class Handler(webapp2.RequestHandler):
    def renderError(self, error_code):
        self.error(error_code)
        self.response.write("Something's wrong! Help!")

class Blog(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC")
        t = jinja_env.get_template("main-blog.html")
        content = t.render(blogs = blogs)
        self.response.write(content)

class NewPost(Handler):
    def get(self):
        t = jinja_env.get_template("new-post.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        new_blog_title = self.request.get("title")
        new_blog_body = self.request.get("text")

        if (not new_blog_title) or (new_blog_title.strip() == ""):
            error = "Please give your blog a title."
        else:
            error = ""
            # self.redirect("/new-post?error=" + cgi.escape(error))

        if (not new_blog_body) or (new_blog_body.strip() == ""):
            error = "Please write something."
        else:
            error = ""
            # self.redirect("/new-post?error=" + cgi.escape(error))

        blogs = Blogpost(title = new_blog_title, text = new_blog_body)
        blogs.put()

        self.redirect("/blog")

app = webapp2.WSGIApplication([
    ('/blog', Blog),
    ('/new-post', NewPost)
], debug=True)
