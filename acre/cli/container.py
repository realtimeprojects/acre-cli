import logging


class Container:
    def __init__(self, docker, args):
        self.docker = docker
        self.args = args

    def exec(self, **kwargs):
        self.start()
        self.docker.exec(**kwargs)
        self.stop()

    def stop(self, force=False):
        if not self.args.stop and not force:
            return
        if not self.docker.is_running():
            return
        self.docker.stop()

    def start(self):
        if self.args.rebuild:
            if self.docker.is_running():
                logging.warning("stopping running container")
                self.docker.stop()
            ec = self.docker.build(update=self.args.update)
            if ec:
                raise Exception("failed to build docker container")

        if self.docker.is_running():
            if self.args.restart:
                self.docker.stop()
                self.docker.run(mounts=self.args.mount)
        else:
            self.docker.run(mounts=self.args.mount)
