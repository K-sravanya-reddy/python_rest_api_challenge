import json
import os

import falcon
import psycopg2
import psycopg2.extras


class HealthHandler(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200


class TodosHandler(object):

    def on_get(self, req, resp):
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM public.todo")
        todos = cur.fetchall()
        cur.close()
        conn.close()
        resp.set_header('Content-Type', 'application/json')
        resp.body = json.dumps(todos, sort_keys=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        body = json.loads(req.req_body)
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor()
        cur.execute("INSERT INTO public.todo (title, status) VALUES ('{}', '{}')"
            .format(body['title'], body['status']))
        conn.commit()
        cur.close()
        conn.close()
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):
        body = json.loads(req.req_body)
        conn = psycopg2.connect(host=os.environ["DB_HOST"],
                                dbname=os.environ["DB_NAME"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        todo_body = "SELECT * FROM public.todo where id={}".format(body['id'])

        if todo_body is None:
            cur.execute("INSERT INTO public.todo (title, status) VALUES ('{}', '{}')"
                        .format(body['title'], body['status']))
            conn.commit()
            cur.close()
            conn.close()
            resp.status = falcon.HTTP_200
        else:
            cur.execute("UPDATE public.todo SET(title={}, status={}) WHERE id={}"
                        .format(body['title'], body['status'], body['id']))
            conn.commit()
            cur.close()
            conn.close()
            resp.status = falcon.HTTP_200






