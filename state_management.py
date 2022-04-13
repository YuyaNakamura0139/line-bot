class Status:
    def __init__(self):
        self.context = "0"
        self.day = ""

    def get_context(self):
        return self.context

    def set_context(self, context):
        self.context = context

    def set_day(self, day):
        self.day = day

    def get_day(self):
        return self.day


class MySession:
    _status_map = dict()

    def register(self, user_id):
        """key:user_id,value:Statusインスタンスとして_status_mapに登録"""
        if self._get_status(user_id) is None:
            self._put_status(user_id, Status())

    def reset(self, user_id):
        """user_idに一致するstatusを初期化する"""
        self._put_status(user_id, Status())

    def _get_status(self, user_id):
        """user_idに一致するstatusを返す"""
        return self._status_map.get(user_id)

    def _put_status(self, user_id, status: Status):
        """statusを_status_mapに登録"""
        self._status_map[user_id] = status

    def read_context(self, user_id):
        """context属性を返す"""
        return self._status_map.get(user_id).get_context()

    def update_context(self, user_id, context):
        new_status = self._status_map.get(user_id)
        new_status.set_context(context)
        self._status_map[user_id] = new_status
