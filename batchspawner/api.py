import json
from tornado import web
from jupyterhub.apihandlers import  APIHandler, default_handlers

class BatchSpawnerAPIHandler(APIHandler):
    @web.authenticated
    def post(self):
        """POST set user spawner data"""
        if hasattr(self, 'current_user'):
            # Jupyterhub compatability, (september 2018, d79a99323ef1d)
            user = self.current_user
        else:
            # Previous jupyterhub, 0.9.4 and before.
            user = self.get_current_user()
        data = self.get_json_body()
        if self.allow_named_servers:
            server_name = data.pop("server_name", "")
            spawner = user.spawners[server_name]
        else:
            spawner = user.spawner
        for key, value in data.items():
            if hasattr(spawner, key):
                setattr(spawner, key, value)
        self.finish(json.dumps({"message": "BatchSpawner data configured"}))
        self.set_status(201)

default_handlers.append((r"/api/batchspawner", BatchSpawnerAPIHandler))
